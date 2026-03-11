from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PatientViewSet, AppointmentViewSet, StationViewSet, BedViewSet, dashboard_stats

router = DefaultRouter()
router.register(r'patients',     PatientViewSet,     basename='patient')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'stations',     StationViewSet,     basename='station')
router.register(r'beds',         BedViewSet,         basename='bed')

urlpatterns = [
    path('dashboard-stats/', dashboard_stats, name='dashboard-stats'),
] + router.urls
