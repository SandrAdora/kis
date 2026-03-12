from rest_framework import viewsets, filters
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.utils import timezone

from .models import OperationRoom, Operation, AnesthesiaProtocol, OperationReport
from .serializers import (
    OperationRoomSerializer, OperationSerializer, OperationListSerializer,
    AnesthesiaProtocolSerializer, OperationReportSerializer,
)
from administrative.models import Patient
from clinical.models import (
    Allergy, PreExistingCondition, Surgery,
    Prescription, Diagnosis, LabResult, VitalSigns, ClinicalNote,
)
from clinical.serializers import (
    AllergySerializer, PreExistingConditionSerializer, SurgerySerializer,
    PrescriptionSerializer, DiagnosisSerializer, LabResultSerializer,
    VitalSignsSerializer, ClinicalNoteSerializer,
)


class OperationRoomViewSet(viewsets.ModelViewSet):
    queryset         = OperationRoom.objects.all()
    serializer_class = OperationRoomSerializer


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.select_related('patient', 'operation_room', 'admission').all()

    def get_serializer_class(self):
        if self.action == 'list':
            return OperationListSerializer
        return OperationSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        p  = self.request.query_params
        if p.get('patient'):
            qs = qs.filter(patient=p['patient'])
        if p.get('date'):
            qs = qs.filter(planned_date=p['date'])
        if p.get('status'):
            qs = qs.filter(status=p['status'])
        if p.get('room'):
            qs = qs.filter(operation_room=p['room'])
        return qs


class AnesthesiaProtocolViewSet(viewsets.ModelViewSet):
    queryset         = AnesthesiaProtocol.objects.select_related('operation').all()
    serializer_class = AnesthesiaProtocolSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        op = self.request.query_params.get('operation')
        if op:
            qs = qs.filter(operation=op)
        return qs


class OperationReportViewSet(viewsets.ModelViewSet):
    queryset         = OperationReport.objects.select_related('operation').all()
    serializer_class = OperationReportSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        op = self.request.query_params.get('operation')
        if op:
            qs = qs.filter(operation=op)
        return qs


@api_view(['GET'])
def operation_dashboard(request):
    today = timezone.localdate()
    total        = Operation.objects.count()
    today_ops    = Operation.objects.filter(planned_date=today).count()
    planned      = Operation.objects.filter(status='planned').count()
    in_progress  = Operation.objects.filter(status='in_progress').count()
    completed    = Operation.objects.filter(status='completed').count()
    emergency    = Operation.objects.filter(priority='emergency', status='planned').count()

    rooms_total     = OperationRoom.objects.count()
    rooms_available = OperationRoom.objects.filter(status='available').count()
    rooms_occupied  = OperationRoom.objects.filter(status='occupied').count()

    today_list = OperationListSerializer(
        Operation.objects.filter(planned_date=today).select_related('patient', 'operation_room'),
        many=True
    ).data

    next_ops = OperationListSerializer(
        Operation.objects.filter(planned_date__gte=today, status__in=['planned','in_progress'])
                         .select_related('patient', 'operation_room')[:10],
        many=True
    ).data

    return Response({
        'total_operations':   total,
        'today_operations':   today_ops,
        'planned':            planned,
        'in_progress':        in_progress,
        'completed':          completed,
        'emergency_pending':  emergency,
        'rooms_total':        rooms_total,
        'rooms_available':    rooms_available,
        'rooms_occupied':     rooms_occupied,
        'today_list':         today_list,
        'next_operations':    next_ops,
    })


@api_view(['GET'])
def patient_preop_summary(request, patient_id):
    """
    Returns a pre-operative anamnesis summary for a patient.
    Aggregates allergies, conditions, past surgeries, active medications,
    active diagnoses, recent lab results, latest vitals, and relevant notes.
    """
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        raise NotFound('Patient nicht gefunden.')

    # Latest vital signs record
    latest_vitals = VitalSigns.objects.filter(patient=patient).first()

    # Recent lab results (last 10)
    recent_labs = LabResult.objects.filter(patient=patient).order_by('-sample_date')[:10]

    # Active prescriptions
    active_prescriptions = Prescription.objects.filter(patient=patient, status='active')

    # Active & chronic diagnoses
    active_diagnoses = Diagnosis.objects.filter(patient=patient, status__in=['active', 'chronic'])

    # All allergies
    allergies = Allergy.objects.filter(patient=patient)

    # Pre-existing conditions
    conditions = PreExistingCondition.objects.filter(patient=patient)

    # Past surgeries
    past_surgeries = Surgery.objects.filter(patient=patient)

    # Relevant anamnesis notes (initial examination notes)
    anamnesis_notes = ClinicalNote.objects.filter(
        patient=patient, note_type__in=['initial', 'followup']
    ).order_by('-created_at')[:5]

    return Response({
        'patient_id':   patient.id,
        'patient_name': f"{patient.last_name}, {patient.first_name}",
        'date_of_birth': str(patient.date_of_birth),

        'allergies':             AllergySerializer(allergies, many=True).data,
        'conditions':            PreExistingConditionSerializer(conditions, many=True).data,
        'past_surgeries':        SurgerySerializer(past_surgeries, many=True).data,
        'active_prescriptions':  PrescriptionSerializer(active_prescriptions, many=True).data,
        'active_diagnoses':      DiagnosisSerializer(active_diagnoses, many=True).data,
        'recent_lab_results':    LabResultSerializer(recent_labs, many=True).data,
        'latest_vitals':         VitalSignsSerializer(latest_vitals).data if latest_vitals else None,
        'anamnesis_notes':       ClinicalNoteSerializer(anamnesis_notes, many=True).data,
    })
