from django.contrib import admin
from .models import ImportBatch, EmissionRecord, DataFlag, ApprovalLog


@admin.register(ImportBatch)
class ImportBatchAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'source_type', 'status', 'rows_total', 'rows_succeeded', 'imported_at']
    list_filter = ['source_type', 'status']


@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_type', 'raw_value', 'scope', 'status', 'created_at']
    list_filter = ['source_type', 'status', 'scope']


@admin.register(DataFlag)
class DataFlagAdmin(admin.ModelAdmin):
    list_display = ['source_type', 'field_name', 'rule_type', 'threshold_value', 'active']


@admin.register(ApprovalLog)
class ApprovalLogAdmin(admin.ModelAdmin):
    list_display = ['record', 'action', 'performed_by', 'performed_at']