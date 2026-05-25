from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImportBatchViewSet, EmissionRecordViewSet

router = DefaultRouter()
router.register(r'batches', ImportBatchViewSet, basename='batch')
router.register(r'records', EmissionRecordViewSet, basename='record')

urlpatterns = [
    path('', include(router.urls)),
]