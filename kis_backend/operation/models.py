from django.db import models
from administrative.models import Patient
from clinical.models import Admission


# ─────────────────────────────────────────────
# OP-Saal
# ─────────────────────────────────────────────
class OperationRoom(models.Model):
    STATUS_CHOICES = [
        ('available',   'Verfügbar'),
        ('occupied',    'Belegt'),
        ('cleaning',    'Reinigung'),
        ('maintenance', 'Außer Betrieb'),
    ]

    name        = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    floor       = models.CharField(max_length=50, blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.name


# ─────────────────────────────────────────────
# Operation
# ─────────────────────────────────────────────
class Operation(models.Model):
    STATUS_CHOICES = [
        ('planned',     'Geplant'),
        ('in_progress', 'In Durchführung'),
        ('completed',   'Abgeschlossen'),
        ('cancelled',   'Abgesagt'),
        ('postponed',   'Verschoben'),
    ]
    PRIORITY_CHOICES = [
        ('elective',  'Elektiv'),
        ('urgent',    'Dringend'),
        ('emergency', 'Notfall'),
    ]

    patient              = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='operations')
    admission            = models.ForeignKey(Admission, on_delete=models.SET_NULL, null=True, blank=True, related_name='operations')
    operation_room       = models.ForeignKey(OperationRoom, on_delete=models.SET_NULL, null=True, blank=True, related_name='operations')

    name                 = models.CharField(max_length=255, help_text='Bezeichnung des Eingriffs')
    ops_code             = models.CharField(max_length=20, blank=True)
    icd_code             = models.CharField(max_length=20, blank=True)
    indication           = models.TextField(blank=True, help_text='Indikation / Diagnose')

    planned_date         = models.DateField()
    planned_start        = models.TimeField()
    planned_duration_min = models.PositiveIntegerField(default=60, help_text='Geplante Dauer in Minuten')

    actual_start         = models.DateTimeField(null=True, blank=True)
    actual_end           = models.DateTimeField(null=True, blank=True)

    status               = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    priority             = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='elective')

    lead_surgeon         = models.CharField(max_length=100)
    assistant_surgeon    = models.CharField(max_length=100, blank=True)
    anesthesiologist     = models.CharField(max_length=100, blank=True)
    scrub_nurse          = models.CharField(max_length=100, blank=True)

    preop_notes          = models.TextField(blank=True)
    postop_notes         = models.TextField(blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['planned_date', 'planned_start']

    def __str__(self):
        return f"{self.name} – {self.patient} ({self.planned_date})"

    @property
    def duration_actual_min(self):
        if self.actual_start and self.actual_end:
            return round((self.actual_end - self.actual_start).total_seconds() / 60)
        return None


# ─────────────────────────────────────────────
# Narkoseprotokoll
# ─────────────────────────────────────────────
class AnesthesiaProtocol(models.Model):
    TYPE_CHOICES = [
        ('general',   'Vollnarkose'),
        ('regional',  'Regionalanästhesie'),
        ('spinal',    'Spinalanästhesie'),
        ('epidural',  'Epiduralanästhesie'),
        ('local',     'Lokalanästhesie'),
        ('sedation',  'Sedierung'),
        ('other',     'Sonstiges'),
    ]
    ASA_CHOICES = [
        ('I',   'ASA I – Gesund'),
        ('II',  'ASA II – Leichte Erkrankung'),
        ('III', 'ASA III – Schwere Erkrankung'),
        ('IV',  'ASA IV – Lebensbedrohliche Erkrankung'),
        ('V',   'ASA V – Moribund'),
    ]

    operation          = models.OneToOneField(Operation, on_delete=models.CASCADE, related_name='anesthesia')
    anesthesia_type    = models.CharField(max_length=20, choices=TYPE_CHOICES, default='general')
    asa_classification = models.CharField(max_length=5, choices=ASA_CHOICES, blank=True)
    anesthesiologist   = models.CharField(max_length=100)
    induction_agent    = models.CharField(max_length=150, blank=True)
    maintenance_agent  = models.CharField(max_length=150, blank=True)
    muscle_relaxant    = models.CharField(max_length=150, blank=True)
    start_time         = models.DateTimeField(null=True, blank=True)
    end_time           = models.DateTimeField(null=True, blank=True)
    premedication      = models.TextField(blank=True)
    intraop_events     = models.TextField(blank=True)
    recovery_notes     = models.TextField(blank=True)
    complications      = models.TextField(blank=True)
    notes              = models.TextField(blank=True)
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Narkose – {self.operation}"


# ─────────────────────────────────────────────
# OP-Bericht
# ─────────────────────────────────────────────
class OperationReport(models.Model):
    operation           = models.OneToOneField(Operation, on_delete=models.CASCADE, related_name='report')
    author              = models.CharField(max_length=100)
    procedure_details   = models.TextField()
    findings            = models.TextField(blank=True)
    specimen            = models.CharField(max_length=255, blank=True)
    blood_loss_ml       = models.PositiveIntegerField(null=True, blank=True)
    transfusions        = models.CharField(max_length=255, blank=True)
    complications       = models.TextField(blank=True)
    closing_technique   = models.CharField(max_length=255, blank=True)
    drains              = models.CharField(max_length=255, blank=True)
    postop_instructions = models.TextField(blank=True)
    created_at          = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OP-Bericht – {self.operation}"
