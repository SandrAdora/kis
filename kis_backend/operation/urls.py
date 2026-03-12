from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OperationRoomViewSet, OperationViewSet,
    AnesthesiaProtocolViewSet, OperationReportViewSet,
    operation_dashboard, patient_preop_summary,
)

router = DefaultRouter()
router.register('rooms',     OperationRoomViewSet,       basename='room')
router.register('operations',OperationViewSet,           basename='operation')
router.register('anesthesia',AnesthesiaProtocolViewSet,  basename='anesthesia')
router.register('reports',   OperationReportViewSet,     basename='report')

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', operation_dashboard),
    path('patients/<int:patient_id>/preop-summary/', patient_preop_summary),
]
