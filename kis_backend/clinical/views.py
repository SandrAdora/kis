from rest_framework import viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from administrative.models import Patient
from .models import (Admission, Diagnosis, Prescription, LabResult, VitalSigns,
                     Allergy, PreExistingCondition, Surgery,
                     ClinicalNote, Procedure, Referral, DischargeLetter)
from .serializers import (AdmissionSerializer, DiagnosisSerializer, PrescriptionSerializer,
                           LabResultSerializer, VitalSignsSerializer, AllergySerializer,
                           PreExistingConditionSerializer, SurgerySerializer,
                           ClinicalNoteSerializer, ProcedureSerializer,
                           ReferralSerializer, DischargeLetterSerializer,
                           PatientClinicalSummarySerializer)


@api_view(['GET'])
def patient_clinical_summary(request, patient_id):
    """Returns all clinical data for a patient in a single request."""
    try:
        patient = Patient.objects.get(pk=patient_id)
    except Patient.DoesNotExist:
        return Response({'error': 'Patient not found'}, status=404)

    data = {
        'admissions':    patient.admissions.all(),
        'diagnoses':     patient.diagnoses.all(),
        'prescriptions': patient.prescriptions.all(),
        'lab_results':   patient.lab_results.all(),
        'vital_signs':   patient.vital_signs.all(),
        'allergies':     patient.allergies.all(),
        'conditions':    patient.conditions.all(),
        'surgeries':     patient.surgeries.all(),
        'notes':         patient.notes.all(),
        'procedures':    patient.procedures.all(),
        'referrals':     patient.referrals.all(),
    }
    serializer = PatientClinicalSummarySerializer(data)
    return Response(serializer.data)


class FilterByPatientMixin:
    """Allows ?patient=<id> query param on any ViewSet."""
    def get_queryset(self):
        qs = super().get_queryset()
        patient = self.request.query_params.get('patient')
        admission = self.request.query_params.get('admission')
        if patient:
            qs = qs.filter(patient=patient)
        if admission and hasattr(qs.model, 'admission'):
            qs = qs.filter(admission=admission)
        return qs


class AdmissionViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Admission.objects.select_related('patient', 'bed').all()
    serializer_class = AdmissionSerializer


class DiagnosisViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Diagnosis.objects.select_related('patient', 'admission').all()
    serializer_class = DiagnosisSerializer


class PrescriptionViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Prescription.objects.select_related('patient', 'admission').all()
    serializer_class = PrescriptionSerializer


class LabResultViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = LabResult.objects.select_related('patient', 'admission').all()
    serializer_class = LabResultSerializer


class VitalSignsViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = VitalSigns.objects.select_related('patient', 'admission').all()
    serializer_class = VitalSignsSerializer


class AllergyViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Allergy.objects.select_related('patient').all()
    serializer_class = AllergySerializer


class PreExistingConditionViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = PreExistingCondition.objects.select_related('patient').all()
    serializer_class = PreExistingConditionSerializer


class SurgeryViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Surgery.objects.select_related('patient').all()
    serializer_class = SurgerySerializer


class ClinicalNoteViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = ClinicalNote.objects.select_related('patient', 'admission', 'appointment').all()
    serializer_class = ClinicalNoteSerializer


class ProcedureViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Procedure.objects.select_related('patient', 'admission').all()
    serializer_class = ProcedureSerializer


class ReferralViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = Referral.objects.select_related('patient', 'admission').all()
    serializer_class = ReferralSerializer


class DischargeLetterViewSet(FilterByPatientMixin, viewsets.ModelViewSet):
    queryset = DischargeLetter.objects.select_related('patient', 'admission').all()
    serializer_class = DischargeLetterSerializer
