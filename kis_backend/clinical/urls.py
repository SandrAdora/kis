from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (AdmissionViewSet, DiagnosisViewSet, PrescriptionViewSet,
                    LabResultViewSet, VitalSignsViewSet, AllergyViewSet,
                    PreExistingConditionViewSet, SurgeryViewSet,
                    ClinicalNoteViewSet, ProcedureViewSet,
                    ReferralViewSet, DischargeLetterViewSet,
                    patient_clinical_summary)

router = DefaultRouter()
router.register(r'admissions',   AdmissionViewSet,            basename='admission')
router.register(r'diagnoses',    DiagnosisViewSet,            basename='diagnosis')
router.register(r'prescriptions',PrescriptionViewSet,         basename='prescription')
router.register(r'lab-results',  LabResultViewSet,            basename='labresult')
router.register(r'vitals',       VitalSignsViewSet,           basename='vitals')
router.register(r'allergies',    AllergyViewSet,              basename='allergy')
router.register(r'conditions',   PreExistingConditionViewSet, basename='condition')
router.register(r'surgeries',    SurgeryViewSet,              basename='surgery')
router.register(r'notes',        ClinicalNoteViewSet,         basename='note')
router.register(r'procedures',   ProcedureViewSet,            basename='procedure')
router.register(r'referrals',    ReferralViewSet,             basename='referral')
router.register(r'discharge-letters', DischargeLetterViewSet, basename='discharge-letter')

urlpatterns = [
    path('patients/<int:patient_id>/summary/', patient_clinical_summary, name='patient-clinical-summary'),
] + router.urls
