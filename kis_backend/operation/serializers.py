from rest_framework import serializers
from .models import OperationRoom, Operation, AnesthesiaProtocol, OperationReport


class OperationRoomSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model  = OperationRoom
        fields = '__all__'


class OperationSerializer(serializers.ModelSerializer):
    status_display   = serializers.CharField(source='get_status_display',   read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    patient_name     = serializers.SerializerMethodField()
    room_name        = serializers.SerializerMethodField()
    duration_actual_min = serializers.ReadOnlyField()
    has_anesthesia   = serializers.SerializerMethodField()
    has_report       = serializers.SerializerMethodField()

    class Meta:
        model  = Operation
        fields = '__all__'

    def get_patient_name(self, obj):
        return f"{obj.patient.last_name}, {obj.patient.first_name}"

    def get_room_name(self, obj):
        return obj.operation_room.name if obj.operation_room else None

    def get_has_anesthesia(self, obj):
        return hasattr(obj, 'anesthesia')

    def get_has_report(self, obj):
        return hasattr(obj, 'report')


class OperationListSerializer(serializers.ModelSerializer):
    status_display   = serializers.CharField(source='get_status_display',   read_only=True)
    priority_display = serializers.CharField(source='get_priority_display', read_only=True)
    patient_name     = serializers.SerializerMethodField()
    room_name        = serializers.SerializerMethodField()

    class Meta:
        model  = Operation
        fields = ['id', 'name', 'ops_code', 'patient', 'patient_name', 'planned_date',
                  'planned_start', 'planned_duration_min', 'status', 'status_display',
                  'priority', 'priority_display', 'lead_surgeon', 'operation_room', 'room_name']

    def get_patient_name(self, obj):
        return f"{obj.patient.last_name}, {obj.patient.first_name}"

    def get_room_name(self, obj):
        return obj.operation_room.name if obj.operation_room else None


class AnesthesiaProtocolSerializer(serializers.ModelSerializer):
    anesthesia_type_display    = serializers.CharField(source='get_anesthesia_type_display', read_only=True)
    asa_classification_display = serializers.CharField(source='get_asa_classification_display', read_only=True)

    class Meta:
        model  = AnesthesiaProtocol
        fields = '__all__'


class OperationReportSerializer(serializers.ModelSerializer):
    class Meta:
        model  = OperationReport
        fields = '__all__'
