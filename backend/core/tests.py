from decimal import Decimal

from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework import status
from rest_framework.test import APITestCase

from .models import ApprovalLog, EmissionRecord, ImportBatch


class UploadEndpointTests(APITestCase):
    def _upload(self, path, filename, content_bytes):
        upload = SimpleUploadedFile(filename, content_bytes, content_type='text/csv')
        return self.client.post(path, {'file': upload}, format='multipart')

    def test_upload_alias_path_accepts_sap_fuel(self):
        content = (
            "WERKS,BWART,MATNR,MENGE,MEINS,BUDAT\n"
            "1000,GI,DIESEL,10,L,2026-01-01\n"
        ).encode('utf-8')
        response = self._upload('/api/upload/sap-fuel/', 'sap_fuel.csv', content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ImportBatch.objects.count(), 1)
        self.assertEqual(ImportBatch.objects.first().source_type, 'SAP_FUEL')
        self.assertEqual(response.data['succeeded'], 1)
        self.assertEqual(response.data['failed'], 0)

    def test_upload_rejects_missing_required_headers(self):
        content = "foo,bar\n1,2\n".encode('utf-8')
        response = self._upload('/api/upload/sap-fuel/', 'bad_headers.csv', content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('missing_headers', response.data)
        self.assertIn('WERKS', response.data['missing_headers'])

    def test_upload_rejects_invalid_utf8(self):
        response = self._upload('/api/upload/sap-fuel/', 'invalid.csv', b'\xff\xfe\xfd')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


class ApprovalWorkflowTests(APITestCase):
    def setUp(self):
        self.batch = ImportBatch.objects.create(
            source_type='SAP_FUEL',
            file_name='batch.csv',
            rows_total=2,
            rows_succeeded=2,
            rows_failed=0,
            status='IMPORTED',
        )

    def _create_record(self, status_value='PENDING'):
        return EmissionRecord.objects.create(
            batch=self.batch,
            source_type='SAP_FUEL',
            source_location_code='1000',
            source_location_type='SAP_PLANT',
            raw_data={'WERKS': '1000', 'MATNR': 'DIESEL'},
            raw_value=Decimal('10.0'),
            raw_unit='L',
            normalized_value=Decimal('26.8'),
            normalized_unit='kg CO2/L',
            conversion_factor=Decimal('2.680000'),
            conversion_factor_source='IPCC AR6 GWP100',
            scope='SCOPE_1',
            activity_type='diesel_combustion',
            status=status_value,
        )

    def test_approve_batch_is_idempotent(self):
        self._create_record('PENDING')
        self._create_record('PENDING')

        first = self.client.post(
            f'/api/batches/{self.batch.id}/approve-batch/',
            {'performed_by': 'qa'},
            format='json',
        )
        second = self.client.post(
            f'/api/batches/{self.batch.id}/approve-batch/',
            {'performed_by': 'qa'},
            format='json',
        )

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(first.data['count'], 2)
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(second.data['count'], 0)
        self.assertEqual(ApprovalLog.objects.count(), 2)
        self.assertFalse(self.batch.records.exclude(status='APPROVED').exists())

    def test_single_record_approve_is_idempotent(self):
        record = self._create_record('PENDING')

        first = self.client.post(f'/api/records/{record.id}/approve/', {'performed_by': 'qa'}, format='json')
        second = self.client.post(f'/api/records/{record.id}/approve/', {'performed_by': 'qa'}, format='json')

        self.assertEqual(first.status_code, status.HTTP_200_OK)
        self.assertEqual(first.data['status'], 'approved')
        self.assertEqual(second.status_code, status.HTTP_200_OK)
        self.assertEqual(second.data['status'], 'already_approved')
        self.assertEqual(ApprovalLog.objects.filter(record=record, action='APPROVED').count(), 1)


class RecordsPaginationTests(APITestCase):
    def test_batch_records_endpoint_returns_paginated_payload(self):
        batch = ImportBatch.objects.create(
            source_type='SAP_FUEL',
            file_name='many.csv',
            rows_total=55,
            rows_succeeded=55,
            rows_failed=0,
            status='IMPORTED',
        )
        for _ in range(55):
            EmissionRecord.objects.create(
                batch=batch,
                source_type='SAP_FUEL',
                source_location_code='1000',
                source_location_type='SAP_PLANT',
                raw_data={'WERKS': '1000', 'MATNR': 'DIESEL'},
                raw_value=Decimal('10.0'),
                raw_unit='L',
                normalized_value=Decimal('26.8'),
                normalized_unit='kg CO2/L',
                conversion_factor=Decimal('2.680000'),
                conversion_factor_source='IPCC AR6 GWP100',
                scope='SCOPE_1',
                activity_type='diesel_combustion',
                status='PENDING',
            )

        response = self.client.get(f'/api/batches/{batch.id}/records/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('count', response.data)
        self.assertIn('results', response.data)
        self.assertEqual(response.data['count'], 55)
        self.assertEqual(len(response.data['results']), 50)
        self.assertIsNotNone(response.data['next'])
