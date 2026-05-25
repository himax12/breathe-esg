import uuid
from django.db import models


class ImportBatch(models.Model):
    SOURCE_TYPES = [
        ('SAP_FUEL', 'SAP Fuel'),
        ('SAP_PROCUREMENT', 'SAP Procurement'),
        ('UTILITY_ELECTRICITY', 'Utility Electricity'),
        ('CORPORATE_TRAVEL', 'Corporate Travel'),
    ]
    STATUS_TYPES = [
        ('UPLOADING', 'Uploading'),
        ('VALIDATING', 'Validating'),
        ('IMPORTED', 'Imported'),
        ('REVIEW_IN_PROGRESS', 'Review In Progress'),
        ('COMPLETED', 'Completed'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPES)
    file_name = models.CharField(max_length=255)
    rows_total = models.IntegerField(default=0)
    rows_succeeded = models.IntegerField(default=0)
    rows_failed = models.IntegerField(default=0)
    status = models.CharField(max_length=30, choices=STATUS_TYPES, default='UPLOADING')
    total_kgCO2_scope1 = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    total_kgCO2_scope2_location = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    total_kgCO2_scope3 = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    imported_by = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-imported_at']
    
    def __str__(self):
        return f"{self.source_type} - {self.file_name} ({self.rows_total} rows)"


class EmissionRecord(models.Model):
    SOURCE_TYPES = [
        ('SAP_FUEL', 'SAP Fuel'),
        ('SAP_PROCUREMENT', 'SAP Procurement'),
        ('UTILITY_ELECTRICITY', 'Utility Electricity'),
        ('CORPORATE_TRAVEL', 'Corporate Travel'),
    ]
    LOCATION_TYPES = [
        ('SAP_PLANT', 'SAP Plant'),
        ('UTILITY_METER', 'Utility Meter'),
        ('AIRPORT', 'Airport'),
    ]
    STATUS_TYPES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged'),
        ('REJECTED', 'Rejected'),
    ]
    SCOPE_TYPES = [
        ('SCOPE_1', 'Scope 1'),
        ('SCOPE_2_LOCATION', 'Scope 2 (Location-Based)'),
        ('SCOPE_3', 'Scope 3'),
    ]
    FLAG_TYPES = [
        ('MISSING_FIELD', 'Missing Required Field'),
        ('VALUE_OUT_OF_RANGE', 'Value Out of Range'),
        ('OTHER', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    batch = models.ForeignKey(ImportBatch, on_delete=models.CASCADE, related_name='records')
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPES)
    source_location_code = models.CharField(max_length=100, null=True, blank=True)
    source_location_type = models.CharField(max_length=20, choices=LOCATION_TYPES, null=True, blank=True)
    raw_data = models.JSONField()
    raw_value = models.DecimalField(max_digits=15, decimal_places=4)
    raw_unit = models.CharField(max_length=30)
    normalized_value = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    normalized_unit = models.CharField(max_length=30, null=True, blank=True)
    conversion_factor = models.DecimalField(max_digits=10, decimal_places=6, null=True, blank=True)
    conversion_factor_source = models.CharField(max_length=100, null=True, blank=True)
    scope = models.CharField(max_length=20, choices=SCOPE_TYPES, null=True, blank=True)
    activity_type = models.CharField(max_length=100, null=True, blank=True)
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_TYPES, default='PENDING')
    flag_type = models.CharField(max_length=20, choices=FLAG_TYPES, null=True, blank=True)
    flag_reason = models.TextField(null=True, blank=True)
    flag_score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100, null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.source_type} - {self.raw_value} {self.raw_unit}"


class DataFlag(models.Model):
    SOURCE_TYPES = [
        ('SAP_FUEL', 'SAP Fuel'),
        ('SAP_PROCUREMENT', 'SAP Procurement'),
        ('UTILITY_ELECTRICITY', 'Utility Electricity'),
        ('CORPORATE_TRAVEL', 'Corporate Travel'),
    ]
    RULE_TYPES = [
        ('MIN_VALUE', 'Minimum Value'),
        ('MAX_VALUE', 'Maximum Value'),
        ('REQUIRED', 'Required Field'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    source_type = models.CharField(max_length=30, choices=SOURCE_TYPES)
    field_name = models.CharField(max_length=100)
    rule_type = models.CharField(max_length=20, choices=RULE_TYPES)
    threshold_value = models.DecimalField(max_digits=15, decimal_places=4, null=True, blank=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ['source_type', 'field_name', 'rule_type']
    
    def __str__(self):
        return f"{self.source_type} - {self.field_name} ({self.rule_type})"


class ApprovalLog(models.Model):
    ACTION_TYPES = [
        ('APPROVED', 'Approved'),
        ('FLAGGED', 'Flagged'),
        ('REJECTED', 'Rejected'),
        ('NOTE_ADDED', 'Note Added'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    record = models.ForeignKey(EmissionRecord, on_delete=models.CASCADE, related_name='approval_history')
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    performed_by = models.CharField(max_length=100, default='analyst')
    performed_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(null=True, blank=True)
    
    class Meta:
        ordering = ['performed_at']
    
    def __str__(self):
        return f"{self.record.id} - {self.action} by {self.performed_by}"