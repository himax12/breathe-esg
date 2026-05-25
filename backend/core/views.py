import csv
import io
from decimal import Decimal, InvalidOperation
from datetime import datetime

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from django.db import models, transaction, OperationalError

from .models import ImportBatch, EmissionRecord, DataFlag, ApprovalLog
from .serializers import ImportBatchSerializer, EmissionRecordSerializer, ApprovalLogSerializer
from .utils import get_iata_distance


# Normalization constants (IPCC AR6 GWP100)
NORMALIZATION_FACTORS = {
    'SAP_FUEL': {
        'diesel': {'factor': Decimal('2.68'), 'unit': 'kg CO2/L', 'source': 'IPCC AR6 GWP100'},
        'gasoline': {'factor': Decimal('2.31'), 'unit': 'kg CO2/L', 'source': 'IPCC AR6 GWP100'},
    },
    'UTILITY_ELECTRICITY': {
        'default': {'factor': Decimal('0.42'), 'unit': 'kg CO2/kWh', 'source': 'eGRID 2024 avg'},
    },
    'CORPORATE_TRAVEL': {
        'flight_short': {'factor': Decimal('0.147'), 'unit': 'kg CO2/km', 'source': 'DEFRA 2024'},
        'flight_long': {'factor': Decimal('0.195'), 'unit': 'kg CO2/km', 'source': 'DEFRA 2024'},
        'hotel': {'factor': Decimal('27.1'), 'unit': 'kg CO2/night', 'source': 'EPA 2022'},
        'diesel_car': {'factor': Decimal('0.171'), 'unit': 'kg CO2/km', 'source': 'DEFRA 2024'},
        'petrol_car': {'factor': Decimal('0.156'), 'unit': 'kg CO2/km', 'source': 'DEFRA 2024'},
    },
}

# Default flag rules
DEFAULT_FLAG_RULES = [
    {'source_type': 'SAP_FUEL', 'field_name': 'MENGE', 'rule_type': 'MAX_VALUE', 'threshold_value': '50000'},
    {'source_type': 'SAP_FUEL', 'field_name': 'MEINS', 'rule_type': 'REQUIRED', 'threshold_value': None},
    {'source_type': 'UTILITY_ELECTRICITY', 'field_name': 'meter_id', 'rule_type': 'REQUIRED', 'threshold_value': None},
    {'source_type': 'UTILITY_ELECTRICITY', 'field_name': 'consumption_kwh', 'rule_type': 'MAX_VALUE', 'threshold_value': '50000'},
    {'source_type': 'CORPORATE_TRAVEL', 'field_name': 'distance_km', 'rule_type': 'REQUIRED', 'threshold_value': None},
]

REQUIRED_COLUMNS = {
    'SAP_FUEL': ['WERKS', 'BWART', 'MATNR', 'MENGE', 'MEINS', 'BUDAT'],
    'SAP_PROCUREMENT': ['WERKS', 'MATNR', 'MENGE', 'MEINS', 'BUDAT'],
    'UTILITY_ELECTRICITY': [
        'meter_id',
        'billing_period_start',
        'billing_period_end',
        'consumption_kwh',
        'demand_kva',
        'tariff_code',
    ],
    'CORPORATE_TRAVEL': [
        'employee_id',
        'trip_date',
        'category',
        'origin',
        'destination',
        'distance_km',
        'amount_local',
        'currency',
    ],
}


def get_flag_score(record_data, source_type):
    """Calculate flag score based on threshold rules."""
    score = 0
    flag_type = None
    flag_reason = None
    
    rules = DataFlag.objects.filter(source_type=source_type, active=True)
    
    for rule in rules:
        field_value = record_data.get(rule.field_name)
        
        if rule.rule_type == 'REQUIRED':
            if field_value is None or str(field_value).strip() == '':
                score += 1
                flag_type = 'MISSING_FIELD'
                flag_reason = f"Required field '{rule.field_name}' is missing"
        elif rule.rule_type in ('MIN_VALUE', 'MAX_VALUE') and rule.threshold_value:
            try:
                val = Decimal(str(field_value))
                threshold = Decimal(str(rule.threshold_value))
                if rule.rule_type == 'MAX_VALUE' and val > threshold:
                    score += 1
                    flag_type = 'VALUE_OUT_OF_RANGE'
                    flag_reason = f"Value {val} exceeds maximum {threshold}"
            except (InvalidOperation, TypeError):
                pass
    
    return score, flag_type, flag_reason


def normalize_record(record_data, source_type):
    """Normalize a record based on source type."""
    normalized_value = None
    normalized_unit = None
    conversion_factor = None
    factor_source = None
    scope = None
    activity_type = None
    
    if source_type == 'SAP_FUEL':
        try:
            menge = Decimal(str(record_data.get('MENGE', 0)))
            matnr = str(record_data.get('MATNR', '')).lower()
            if 'gas' in matnr or 'petrol' in matnr or 'benzin' in matnr:
                factor_data = NORMALIZATION_FACTORS['SAP_FUEL']['gasoline']
            else:
                factor_data = NORMALIZATION_FACTORS['SAP_FUEL']['diesel']
            conversion_factor = factor_data['factor']
            factor_source = factor_data['source']
            normalized_value = menge * conversion_factor
            normalized_unit = factor_data['unit']
            scope = 'SCOPE_1'
            activity_type = 'gasoline_combustion' if factor_data is NORMALIZATION_FACTORS['SAP_FUEL']['gasoline'] else 'diesel_combustion'
        except (InvalidOperation, TypeError):
            pass
    
    elif source_type == 'UTILITY_ELECTRICITY':
        try:
            kwh = Decimal(str(record_data.get('consumption_kwh', 0)))
            factor_data = NORMALIZATION_FACTORS['UTILITY_ELECTRICITY']['default']
            conversion_factor = factor_data['factor']
            factor_source = factor_data['source']
            normalized_value = kwh * conversion_factor
            normalized_unit = factor_data['unit']
            scope = 'SCOPE_2_LOCATION'
            activity_type = 'grid_electricity'
        except (InvalidOperation, TypeError):
            pass
    
    elif source_type == 'CORPORATE_TRAVEL':
        category = str(record_data.get('category', '')).upper()
        factor_data = None
        try:
            distance = Decimal(str(record_data.get('distance_km', 0)))

            # If distance is missing/zero for FLIGHT but origin/dest are IATA codes, calculate from coordinates
            if category == 'FLIGHT' and distance == 0:
                origin = str(record_data.get('origin', ''))
                dest = str(record_data.get('destination', ''))
                calc_distance = get_iata_distance(origin, dest)
                if calc_distance:
                    distance = Decimal(str(calc_distance))

            if category == 'FLIGHT':
                if distance < 1500:
                    factor_data = NORMALIZATION_FACTORS['CORPORATE_TRAVEL']['flight_short']
                else:
                    factor_data = NORMALIZATION_FACTORS['CORPORATE_TRAVEL']['flight_long']
                normalized_value = distance * factor_data['factor']
            elif category == 'HOTEL':
                factor_data = NORMALIZATION_FACTORS['CORPORATE_TRAVEL']['hotel']
                nights = Decimal(str(record_data.get('nights', 1)))
                normalized_value = nights * factor_data['factor']
            elif category == 'GROUND':
                factor_data = NORMALIZATION_FACTORS['CORPORATE_TRAVEL']['diesel_car']
                normalized_value = distance * factor_data['factor']
            
            if factor_data:
                normalized_unit = factor_data['unit']
                conversion_factor = factor_data['factor']
                factor_source = factor_data['source']
                scope = 'SCOPE_3'
                activity_type = f"{category.lower()}_travel"
        except (InvalidOperation, TypeError):
            pass
    
    return {
        'normalized_value': normalized_value,
        'normalized_unit': normalized_unit,
        'conversion_factor': conversion_factor,
        'conversion_factor_source': factor_source,
        'scope': scope,
        'activity_type': activity_type,
    }


def get_location_info(record_data, source_type):
    """Extract location information based on source type."""
    if source_type == 'SAP_FUEL':
        return {'code': record_data.get('WERKS', ''), 'type': 'SAP_PLANT'}
    elif source_type == 'UTILITY_ELECTRICITY':
        return {'code': record_data.get('meter_id', ''), 'type': 'UTILITY_METER'}
    elif source_type == 'CORPORATE_TRAVEL':
        return {'code': record_data.get('origin', ''), 'type': 'AIRPORT'}
    return {'code': None, 'type': None}


def parse_date(date_str):
    """Parse date from various formats."""
    if not date_str:
        return None
    for fmt in ('%Y-%m-%d', '%d.%m.%Y', '%d/%m/%Y', '%m/%d/%Y'):
        try:
            return datetime.strptime(str(date_str), fmt).date()
        except ValueError:
            continue
    return None


class ImportBatchViewSet(viewsets.ModelViewSet):
    queryset = ImportBatch.objects.all()
    serializer_class = ImportBatchSerializer
    
    @action(detail=True, methods=['get'])
    def records(self, request, pk=None):
        batch = self.get_object()
        records = batch.records.all()
        status_filter = request.query_params.get('status')
        if status_filter:
            records = records.filter(status=status_filter.upper())
        page = self.paginate_queryset(records)
        if page is not None:
            serializer = EmissionRecordSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = EmissionRecordSerializer(records, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path=r'approve[-_]batch')
    def approve_batch(self, request, pk=None):
        batch = self.get_object()
        performed_by = request.data.get('performed_by', 'analyst')
        note = request.data.get('note', '')
        try:
            with transaction.atomic():
                pending_ids = list(
                    batch.records.select_for_update()
                    .filter(status='PENDING')
                    .values_list('id', flat=True)
                )
                if not pending_ids:
                    return Response({'status': 'approved', 'count': 0, 'message': 'No pending records'})

                updated_count = EmissionRecord.objects.filter(
                    id__in=pending_ids,
                    status='PENDING',
                ).update(status='APPROVED')

                ApprovalLog.objects.bulk_create([
                    ApprovalLog(
                        record_id=record_id,
                        action='APPROVED',
                        performed_by=performed_by,
                        note=note,
                    )
                    for record_id in pending_ids
                ])

                if updated_count:
                    batch.status = 'REVIEW_IN_PROGRESS'
                    batch.save(update_fields=['status'])
                    self._update_batch_aggregates(batch)
        except OperationalError:
            return Response(
                {
                    'error': 'Database is busy processing another approval request. Please retry.',
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response({'status': 'approved', 'count': updated_count})
    
    @action(detail=False, methods=['post'], url_path=r'upload-(?P<source_type>[-\w]+)')
    def upload_csv(self, request, source_type=None):
        source_type_map = {
            'sap-fuel': 'SAP_FUEL',
            'sap_fuel': 'SAP_FUEL',
            'sap-procurement': 'SAP_PROCUREMENT',
            'sap_procurement': 'SAP_PROCUREMENT',
            'utility-electricity': 'UTILITY_ELECTRICITY',
            'utility_electricity': 'UTILITY_ELECTRICITY',
            'corporate-travel': 'CORPORATE_TRAVEL',
            'corporate_travel': 'CORPORATE_TRAVEL',
        }
        source_key = (source_type or '').strip().lower()
        model_source_type = source_type_map.get(source_key)
        if not model_source_type:
            return Response(
                {
                    'error': 'Unsupported source type',
                    'supported': sorted(source_type_map.keys()),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            decoded_file = file_obj.read().decode('utf-8-sig')
        except UnicodeDecodeError:
            return Response(
                {'error': 'File must be a UTF-8 encoded CSV'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reader = csv.DictReader(io.StringIO(decoded_file))
        if not reader.fieldnames:
            return Response({'error': 'CSV header row is missing'}, status=status.HTTP_400_BAD_REQUEST)

        required_headers = REQUIRED_COLUMNS.get(model_source_type, [])
        missing_headers = [header for header in required_headers if header not in reader.fieldnames]
        if missing_headers:
            return Response(
                {
                    'error': 'CSV is missing required headers',
                    'missing_headers': missing_headers,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        batch = ImportBatch.objects.create(
            source_type=model_source_type,
            file_name=file_obj.name,
            rows_total=0,
            rows_succeeded=0,
            rows_failed=0,
            status='VALIDATING'
        )
        
        succeeded = 0
        failed = 0
        row_errors = []
        
        for row in reader:
            try:
                location = get_location_info(row, model_source_type)
                norm = normalize_record(row, model_source_type)
                flag_score, flag_type, flag_reason = get_flag_score(row, model_source_type)
                
                if model_source_type == 'SAP_FUEL':
                    period_start = parse_date(row.get('BUDAT', ''))
                    period_end = period_start
                elif model_source_type == 'UTILITY_ELECTRICITY':
                    period_start = parse_date(row.get('billing_period_start', ''))
                    period_end = parse_date(row.get('billing_period_end', ''))
                elif model_source_type == 'CORPORATE_TRAVEL':
                    period_start = parse_date(row.get('trip_date', ''))
                    period_end = period_start
                else:
                    period_start = None
                    period_end = None
                
                # Get raw value from appropriate field
                raw_val_fields = ['MENGE', 'consumption_kwh', 'distance_km', 'amount_local']
                raw_value = Decimal('0')
                raw_unit = ''
                for field in raw_val_fields:
                    if field in row and row[field]:
                        try:
                            raw_value = Decimal(str(row[field]))
                            break
                        except:
                            pass
                
                # Get raw unit
                if model_source_type == 'SAP_FUEL':
                    raw_unit = row.get('MEINS', 'L')
                elif model_source_type == 'UTILITY_ELECTRICITY':
                    raw_unit = 'kWh'
                elif model_source_type == 'CORPORATE_TRAVEL':
                    travel_category = str(row.get('category', '')).upper()
                    if travel_category in ('FLIGHT', 'GROUND'):
                        raw_unit = 'km'
                    elif travel_category == 'HOTEL':
                        raw_unit = 'night'
                    else:
                        raw_unit = row.get('currency', 'USD')
                
                EmissionRecord.objects.create(
                    batch=batch,
                    source_type=model_source_type,
                    source_location_code=location['code'],
                    source_location_type=location['type'],
                    raw_data=dict(row),
                    raw_value=raw_value,
                    raw_unit=raw_unit,
                    normalized_value=norm['normalized_value'],
                    normalized_unit=norm['normalized_unit'],
                    conversion_factor=norm['conversion_factor'],
                    conversion_factor_source=norm['conversion_factor_source'],
                    scope=norm['scope'],
                    activity_type=norm['activity_type'],
                    period_start=period_start,
                    period_end=period_end,
                    status='FLAGGED' if flag_score > 0 else 'PENDING',
                    flag_type=flag_type,
                    flag_reason=flag_reason,
                    flag_score=flag_score,
                )
                succeeded += 1
            except Exception as e:
                failed += 1
                if len(row_errors) < 20:
                    row_errors.append(str(e))
        
        batch.rows_total = succeeded + failed
        batch.rows_succeeded = succeeded
        batch.rows_failed = failed
        batch.status = 'IMPORTED'
        batch.save()
        
        return Response({
            'batch_id': str(batch.id),
            'total': batch.rows_total,
            'succeeded': batch.rows_succeeded,
            'failed': batch.rows_failed,
            'row_errors': row_errors,
        })
    
    def _update_batch_aggregates(self, batch):
        aggs = batch.records.filter(status='APPROVED').aggregate(
            scope1=Sum('normalized_value', filter=models.Q(scope='SCOPE_1')),
            scope2=Sum('normalized_value', filter=models.Q(scope='SCOPE_2_LOCATION')),
            scope3=Sum('normalized_value', filter=models.Q(scope='SCOPE_3')),
        )
        batch.total_kgCO2_scope1 = aggs['scope1'] or Decimal('0')
        batch.total_kgCO2_scope2_location = aggs['scope2'] or Decimal('0')
        batch.total_kgCO2_scope3 = aggs['scope3'] or Decimal('0')
        batch.save()


class EmissionRecordViewSet(viewsets.ModelViewSet):
    queryset = EmissionRecord.objects.all()
    serializer_class = EmissionRecordSerializer
    
    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        record = self.get_object()
        performed_by = request.data.get('performed_by', 'analyst')
        note = request.data.get('note', '')
        try:
            with transaction.atomic():
                updated_count = EmissionRecord.objects.select_for_update().filter(
                    id=record.id,
                    status__in=['PENDING', 'FLAGGED'],
                ).update(status='APPROVED')
                if not updated_count:
                    return Response({'status': 'already_approved'})
                ApprovalLog.objects.create(
                    record=record,
                    action='APPROVED',
                    performed_by=performed_by,
                    note=note,
                )
        except OperationalError:
            return Response(
                {'error': 'Database is busy processing another approval request. Please retry.'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        # Update batch aggregates
        batch = record.batch
        view = ImportBatchViewSet()
        view._update_batch_aggregates(batch)
        return Response({'status': 'approved'})
    
    @action(detail=True, methods=['post'])
    def flag(self, request, pk=None):
        record = self.get_object()
        record.status = 'FLAGGED'
        record.flag_type = request.data.get('flag_type', 'OTHER')
        record.flag_reason = request.data.get('flag_reason', '')
        record.save()
        ApprovalLog.objects.create(
            record=record,
            action='FLAGGED',
            performed_by=request.data.get('performed_by', 'analyst'),
            note=request.data.get('note', '')
        )
        return Response({'status': 'flagged'})
    
    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        record = self.get_object()
        record.status = 'REJECTED'
        record.save()
        ApprovalLog.objects.create(
            record=record,
            action='REJECTED',
            performed_by=request.data.get('performed_by', 'analyst'),
            note=request.data.get('note', '')
        )
        return Response({'status': 'rejected'})
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        record = self.get_object()
        logs = record.approval_history.all()
        serializer = ApprovalLogSerializer(logs, many=True)
        return Response(serializer.data)
