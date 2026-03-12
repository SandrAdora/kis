from django.db import models
from administrative.models import Patient, Bed, Appointment


# ─────────────────────────────────────────────
# Admission
# ─────────────────────────────────────────────
class Admission(models.Model):
    DISCHARGE_CHOICES = [
        ('home',      'Nach Hause'),
        ('transfer',  'Verlegung'),
        ('deceased',  'Verstorben'),
        ('other',     'Sonstiges'),
    ]

    patient        = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    bed            = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, blank=True, related_name='admissions')
    admission_date = models.DateField()
    discharge_date = models.DateField(null=True, blank=True)
    discharge_type = models.CharField(max_length=20, choices=DISCHARGE_CHOICES, blank=True)
    reason         = models.CharField(max_length=255)
    notes          = models.TextField(blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-admission_date']

    def __str__(self):
        return f"{self.patient} – Aufnahme {self.admission_date}"

    @property
    def is_active(self):
        return self.discharge_date is None


# ─────────────────────────────────────────────
# Diagnosis
# ─────────────────────────────────────────────
class Diagnosis(models.Model):
    TYPE_CHOICES = [
        ('primary',    'Hauptdiagnose'),
        ('secondary',  'Nebendiagnose'),
        ('admission',  'Aufnahmediagnose'),
    ]
    STATUS_CHOICES = [
        ('active',    'Aktiv'),
        ('resolved',  'Abgeklungen'),
        ('chronic',   'Chronisch'),
    ]

    patient    = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='diagnoses')
    admission  = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='diagnoses')
    icd_code   = models.CharField(max_length=20)
    description = models.CharField(max_length=255)
    type       = models.CharField(max_length=20, choices=TYPE_CHOICES, default='primary')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    doctor     = models.CharField(max_length=100, blank=True)
    date       = models.DateField()
    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.icd_code} – {self.description}"


# ─────────────────────────────────────────────
# Medication / Prescription
# ─────────────────────────────────────────────
class Prescription(models.Model):
    ROUTE_CHOICES = [
        ('oral',      'Oral'),
        ('iv',        'Intravenös'),
        ('im',        'Intramuskulär'),
        ('topical',   'Topisch'),
        ('inhaled',   'Inhalativ'),
        ('other',     'Sonstiges'),
    ]
    STATUS_CHOICES = [
        ('active',        'Aktiv'),
        ('discontinued',  'Abgesetzt'),
        ('completed',     'Abgeschlossen'),
    ]

    patient    = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    admission  = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='prescriptions')
    drug_name  = models.CharField(max_length=150)
    dosage     = models.CharField(max_length=50)
    unit       = models.CharField(max_length=30)
    frequency  = models.CharField(max_length=100)
    route      = models.CharField(max_length=20, choices=ROUTE_CHOICES, default='oral')
    start_date = models.DateField()
    end_date   = models.DateField(null=True, blank=True)
    doctor     = models.CharField(max_length=100, blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.drug_name} {self.dosage}{self.unit} – {self.patient}"


# ─────────────────────────────────────────────
# Lab Results
# ─────────────────────────────────────────────
class LabResult(models.Model):
    STATUS_CHOICES = [
        ('normal',   'Normal'),
        ('elevated', 'Erhöht'),
        ('low',      'Erniedrigt'),
        ('critical', 'Kritisch'),
    ]

    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    admission       = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_results')
    test_name       = models.CharField(max_length=150)
    value           = models.CharField(max_length=50)
    unit            = models.CharField(max_length=30, blank=True)
    reference_range = models.CharField(max_length=50, blank=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='normal')
    sample_date     = models.DateField()
    result_date     = models.DateField(null=True, blank=True)
    ordering_doctor = models.CharField(max_length=100, blank=True)
    notes           = models.TextField(blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sample_date']

    def __str__(self):
        return f"{self.test_name}: {self.value} {self.unit} ({self.patient})"


# ─────────────────────────────────────────────
# Vital Signs
# ─────────────────────────────────────────────
class VitalSigns(models.Model):
    patient         = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    admission       = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='vital_signs')
    timestamp       = models.DateTimeField()
    systolic_bp     = models.IntegerField(null=True, blank=True, help_text='mmHg')
    diastolic_bp    = models.IntegerField(null=True, blank=True, help_text='mmHg')
    heart_rate      = models.IntegerField(null=True, blank=True, help_text='bpm')
    temperature     = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text='°C')
    oxygen_sat      = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text='%')
    weight          = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text='kg')
    height          = models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, help_text='cm')
    measured_by     = models.CharField(max_length=100, blank=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Vital Signs'

    @property
    def bmi(self):
        if self.weight and self.height and self.height > 0:
            h_m = float(self.height) / 100
            return round(float(self.weight) / (h_m ** 2), 1)
        return None

    def __str__(self):
        return f"Vitals {self.patient} – {self.timestamp:%d.%m.%Y %H:%M}"


# ─────────────────────────────────────────────
# Medical History
# ─────────────────────────────────────────────
class Allergy(models.Model):
    SEVERITY_CHOICES = [
        ('mild',     'Mild'),
        ('moderate', 'Mittel'),
        ('severe',   'Schwer'),
    ]

    patient   = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='allergies')
    substance = models.CharField(max_length=150)
    reaction  = models.CharField(max_length=255, blank=True)
    severity  = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='mild')
    noted_at  = models.DateField()

    class Meta:
        ordering = ['-severity']
        verbose_name_plural = 'Allergies'

    def __str__(self):
        return f"{self.substance} ({self.severity}) – {self.patient}"


class PreExistingCondition(models.Model):
    patient     = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='conditions')
    name        = models.CharField(max_length=200)
    icd_code    = models.CharField(max_length=20, blank=True)
    since       = models.DateField(null=True, blank=True)
    notes       = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} – {self.patient}"


class Surgery(models.Model):
    patient      = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='surgeries')
    procedure    = models.CharField(max_length=255)
    ops_code     = models.CharField(max_length=20, blank=True)
    date         = models.DateField()
    hospital     = models.CharField(max_length=150, blank=True)
    surgeon      = models.CharField(max_length=100, blank=True)
    notes        = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.procedure} ({self.date}) – {self.patient}"


# ─────────────────────────────────────────────
# Clinical Notes
# ─────────────────────────────────────────────
class ClinicalNote(models.Model):
    NOTE_TYPES = [
        ('initial',    'Erstuntersuchung'),
        ('followup',   'Verlaufsdokumentation'),
        ('discharge',  'Entlassungsnotiz'),
        ('consultation','Konsil'),
        ('other',      'Sonstiges'),
    ]

    patient     = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='notes')
    admission   = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='clinical_notes')
    appointment = models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True, related_name='clinical_notes')
    note_type   = models.CharField(max_length=20, choices=NOTE_TYPES, default='followup')
    content     = models.TextField()
    author      = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_note_type_display()} – {self.patient} ({self.created_at:%d.%m.%Y})"


# ─────────────────────────────────────────────
# Procedures
# ─────────────────────────────────────────────
class Procedure(models.Model):
    patient    = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='procedures')
    admission  = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='procedures')
    ops_code   = models.CharField(max_length=20, blank=True)
    name       = models.CharField(max_length=255)
    date       = models.DateField()
    doctor     = models.CharField(max_length=100, blank=True)
    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.name} – {self.patient} ({self.date})"


# ─────────────────────────────────────────────
# Referrals / Consultations
# ─────────────────────────────────────────────
class Referral(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Ausstehend'),
        ('completed', 'Abgeschlossen'),
        ('cancelled', 'Abgesagt'),
    ]

    patient          = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='referrals')
    admission        = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    referring_doctor = models.CharField(max_length=100)
    specialist       = models.CharField(max_length=100)
    specialty        = models.CharField(max_length=100, blank=True)
    reason           = models.CharField(max_length=255)
    date             = models.DateField()
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_notes     = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Überweisung → {self.specialist} ({self.patient})"


# ─────────────────────────────────────────────
# Discharge Letter
# ─────────────────────────────────────────────
class DischargeLetter(models.Model):
    patient             = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='discharge_letters')
    admission           = models.OneToOneField(Admission, on_delete=models.CASCADE, related_name='discharge_letter')
    diagnosis_summary   = models.TextField()
    treatment_summary   = models.TextField()
    followup_instructions = models.TextField(blank=True)
    medication_on_discharge = models.TextField(blank=True)
    author              = models.CharField(max_length=100)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entlassungsbrief – {self.patient} ({self.created_at:%d.%m.%Y})"
