from rest_framework import serializers
from .models import Patient, Appointment, Station, Bed


class BedSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Bed
        fields = '__all__'

    def get_patient_name(self, obj):
        if obj.patient:
            return f"{obj.patient.last_name}, {obj.patient.first_name}"
        return None


class StationSerializer(serializers.ModelSerializer):
    beds = BedSerializer(many=True, read_only=True)
    total_beds = serializers.ReadOnlyField()
    free_beds = serializers.ReadOnlyField()
    occupied_beds = serializers.ReadOnlyField()

    class Meta:
        model = Station
        fields = '__all__'


class StationListSerializer(serializers.ModelSerializer):
    total_beds = serializers.ReadOnlyField()
    free_beds = serializers.ReadOnlyField()
    occupied_beds = serializers.ReadOnlyField()

    class Meta:
        model = Station
        fields = ['id', 'name', 'description', 'floor', 'total_beds', 'free_beds', 'occupied_beds']


class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()

    class Meta:
        model = Appointment
        fields = '__all__'

    def get_patient_name(self, obj):
        return f"{obj.patient.last_name}, {obj.patient.first_name}"


class PatientSerializer(serializers.ModelSerializer):
    appointments = AppointmentSerializer(many=True, read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = ['id', 'first_name', 'last_name', 'date_of_birth', 'gender',
                  'phone', 'insurance_number', 'insurance_provider']
