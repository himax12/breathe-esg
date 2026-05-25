from django.core.management.base import BaseCommand
from core.models import DataFlag

DEFAULT_FLAG_RULES = [
    {'source_type': 'SAP_FUEL', 'field_name': 'MENGE', 'rule_type': 'MAX_VALUE', 'threshold_value': '50000'},
    {'source_type': 'SAP_FUEL', 'field_name': 'MEINS', 'rule_type': 'REQUIRED', 'threshold_value': None},
    {'source_type': 'UTILITY_ELECTRICITY', 'field_name': 'meter_id', 'rule_type': 'REQUIRED', 'threshold_value': None},
    {'source_type': 'UTILITY_ELECTRICITY', 'field_name': 'consumption_kwh', 'rule_type': 'MAX_VALUE', 'threshold_value': '50000'},
    {'source_type': 'CORPORATE_TRAVEL', 'field_name': 'distance_km', 'rule_type': 'REQUIRED', 'threshold_value': None},
]


class Command(BaseCommand):
    def handle(self, *args, **options):
        for rule in DEFAULT_FLAG_RULES:
            DataFlag.objects.update_or_create(
                source_type=rule['source_type'],
                field_name=rule['field_name'],
                rule_type=rule['rule_type'],
                defaults={
                    'threshold_value': rule['threshold_value'] or None,
                    'active': True,
                }
            )
        self.stdout.write(self.style.SUCCESS('Flag rules seeded'))