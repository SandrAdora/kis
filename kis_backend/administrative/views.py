from django.utils import timezone
from django.db.models import Count, Q
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from .models import Patient, Appointment, Station, Bed
from .serializers import (PatientSerializer, PatientListSerializer,
                           AppointmentSerializer, StationSerializer,
                           StationListSerializer, BedSerializer)


@api_view(['GET'])
def dashboard_stats(request):
    today = timezone.localdate()
    total_patients = Patient.objects.count()
    todays_appointments = Appointment.objects.filter(date=today).count()
    open_appointments = Appointment.objects.filter(status='scheduled').count()
    total_beds = Bed.objects.count()
    free_beds = Bed.objects.filter(status='free').count()
    occupied_beds = Bed.objects.filter(status='occupied').count()
    reserved_beds = Bed.objects.filter(status='reserved').count()

    upcoming = Appointment.objects.filter(
        date__gte=today, status='scheduled'
    ).select_related('patient').order_by('date', 'time')[:10]

    return Response({
        'total_patients': total_patients,
        'todays_appointments': todays_appointments,
        'open_appointments': open_appointments,
        'total_beds': total_beds,
        'free_beds': free_beds,
        'occupied_beds': occupied_beds,
        'reserved_beds': reserved_beds,
        'upcoming_appointments': AppointmentSerializer(upcoming, many=True).data,
    })


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PatientListSerializer
        return PatientSerializer

    @action(detail=True, methods=['get', 'post'], url_path='appointments')
    def appointments(self, request, pk=None):
        patient = self.get_object()
        if request.method == 'GET':
            serializer = AppointmentSerializer(patient.appointments.all(), many=True)
            return Response(serializer.data)
        serializer = AppointmentSerializer(data={**request.data, 'patient': patient.id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.select_related('patient').all()
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        date = self.request.query_params.get('date')
        month = self.request.query_params.get('month')  # YYYY-MM
        week = self.request.query_params.get('week')    # YYYY-WNN
        if date:
            qs = qs.filter(date=date)
        elif month:
            y, m = month.split('-')
            qs = qs.filter(date__year=y, date__month=m)
        elif week:
            from datetime import date as dt, timedelta
            y, w = int(week.split('-W')[0]), int(week.split('-W')[1])
            monday = dt.fromisocalendar(y, w, 1)
            sunday = monday + timedelta(days=6)
            qs = qs.filter(date__range=[monday, sunday])
        return qs


class StationViewSet(viewsets.ModelViewSet):
    queryset = Station.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return StationListSerializer
        return StationSerializer


class BedViewSet(viewsets.ModelViewSet):
    queryset = Bed.objects.select_related('station', 'patient').all()
    serializer_class = BedSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        station = self.request.query_params.get('station')
        if station:
            qs = qs.filter(station=station)
        return qs
