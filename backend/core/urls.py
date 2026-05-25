from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImportBatchViewSet, EmissionRecordViewSet

router = DefaultRouter()
router.register(r'batches', ImportBatchViewSet, basename='batch')
router.register(r'records', EmissionRecordViewSet, basename='record')

upload_csv_view = ImportBatchViewSet.as_view({'post': 'upload_csv'})
approve_batch_view = ImportBatchViewSet.as_view({'post': 'approve_batch'})

urlpatterns = [
    path('upload/<str:source_type>/', upload_csv_view, name='upload-csv-alias'),
    path('batches/<uuid:pk>/approve-batch/', approve_batch_view, name='batch-approve-batch'),
    path('', include(router.urls)),
]
