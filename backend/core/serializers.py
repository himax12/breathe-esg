from rest_framework import serializers
from .models import ImportBatch, EmissionRecord, ApprovalLog


class ApprovalLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApprovalLog
        fields = ['id', 'action', 'performed_by', 'performed_at', 'note']
        read_only_fields = ['id', 'performed_at']


class EmissionRecordSerializer(serializers.ModelSerializer):
    approval_history = ApprovalLogSerializer(many=True, read_only=True)
    
    class Meta:
        model = EmissionRecord
        fields = [
            'id', 'batch', 'source_type', 'source_location_code', 'source_location_type',
            'raw_data', 'raw_value', 'raw_unit', 'normalized_value', 'normalized_unit',
            'conversion_factor', 'conversion_factor_source', 'scope', 'activity_type',
            'period_start', 'period_end', 'status', 'flag_type', 'flag_reason', 'flag_score',
            'created_at', 'created_by', 'approval_history'
        ]
        read_only_fields = ['id', 'created_at', 'approval_history']


class ImportBatchSerializer(serializers.ModelSerializer):
    records_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ImportBatch
        fields = [
            'id', 'source_type', 'file_name', 'rows_total', 'rows_succeeded', 'rows_failed',
            'status', 'total_kgCO2_scope1', 'total_kgCO2_scope2_location', 'total_kgCO2_scope3',
            'imported_at', 'imported_by', 'records_count'
        ]
        read_only_fields = ['id', 'imported_at']
    
    def get_records_count(self, obj):
        return obj.records.count()