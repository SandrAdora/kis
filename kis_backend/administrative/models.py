from django.db import models


class Station(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    floor = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @property
    def total_beds(self):
        return self.beds.count()

    @property
    def free_beds(self):
        return self.beds.filter(status='free').count()

    @property
    def occupied_beds(self):
        return self.beds.filter(status='occupied').count()


class Bed(models.Model):
    STATUS_CHOICES = [
        ('free',        'Frei'),
        ('occupied',    'Belegt'),
        ('reserved',    'Reserviert'),
        ('maintenance', 'Außer Betrieb'),
    ]

    station    = models.ForeignKey(Station, on_delete=models.CASCADE, related_name='beds')
    bed_number = models.CharField(max_length=20)
    room       = models.CharField(max_length=50, blank=True)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free')
    patient    = models.ForeignKey('Patient', on_delete=models.SET_NULL, null=True, blank=True, related_name='beds')
    notes      = models.TextField(blank=True)

    class Meta:
        ordering = ['station', 'room', 'bed_number']

    def __str__(self):
        return f"{self.station.name} – Bett {self.bed_number}"


class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Männlich'),
        ('F', 'Weiblich'),
        ('D', 'Divers'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    insurance_number = models.CharField(max_length=50, blank=True)
    insurance_provider = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Geplant'),
        ('completed', 'Abgeschlossen'),
        ('cancelled', 'Abgesagt'),
    ]

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.CharField(max_length=255)
    doctor = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date', 'time']

    def __str__(self):
        return f"{self.patient} – {self.date} {self.time}"
