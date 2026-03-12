from rest_framework import serializers
from .models import (Admission, Diagnosis, Prescription, LabResult, VitalSigns,
                     Allergy, PreExistingCondition, Surgery,
                     ClinicalNote, Procedure, Referral, DischargeLetter)


class AdmissionSerializer(serializers.ModelSerializer):
    is_active    = serializers.ReadOnlyField()
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model  = Admission
        fields = '__all__'

    def get_patient_name(self, obj):
        return f"{obj.patient.last_name}, {obj.patient.first_name}"


class DiagnosisSerializer(serializers.ModelSerializer):
    type_display   = serializers.CharField(source='get_type_display',   read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Diagnosis
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    route_display  = serializers.CharField(source='get_route_display',  read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Prescription
        fields = '__all__'


class LabResultSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = LabResult
        fields = '__all__'


class VitalSignsSerializer(serializers.ModelSerializer):
    bmi = serializers.ReadOnlyField()

    class Meta:
        model  = VitalSigns
        fields = '__all__'


class AllergySerializer(serializers.ModelSerializer):
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)

    class Meta:
        model  = Allergy
        fields = '__all__'


class PreExistingConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PreExistingCondition
        fields = '__all__'


class SurgerySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Surgery
        fields = '__all__'


class ClinicalNoteSerializer(serializers.ModelSerializer):
    note_type_display = serializers.CharField(source='get_note_type_display', read_only=True)

    class Meta:
        model  = ClinicalNote
        fields = '__all__'


class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Procedure
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = Referral
        fields = '__all__'


class DischargeLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model  = DischargeLetter
        fields = '__all__'


# ── Full patient clinical summary ──────────────────────────────────────────────
class PatientClinicalSummarySerializer(serializers.Serializer):
    """Aggregates all clinical data for a single patient in one response."""
    admissions   = AdmissionSerializer(many=True)
    diagnoses    = DiagnosisSerializer(many=True)
    prescriptions = PrescriptionSerializer(many=True)
    lab_results  = LabResultSerializer(many=True)
    vital_signs  = VitalSignsSerializer(many=True)
    allergies    = AllergySerializer(many=True)
    conditions   = PreExistingConditionSerializer(many=True)
    surgeries    = SurgerySerializer(many=True)
    notes        = ClinicalNoteSerializer(many=True)
    procedures   = ProcedureSerializer(many=True)
    referrals    = ReferralSerializer(many=True)
