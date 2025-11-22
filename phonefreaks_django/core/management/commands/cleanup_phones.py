from django.core.management.base import BaseCommand
from core.models import Phone

class Command(BaseCommand):
    help = 'Clean up phones with empty or invalid IDs'

    def handle(self, *args, **options):
        # Find phones with empty IDs
        invalid_phones = Phone.objects.filter(id='')
        count = invalid_phones.count()
        
        if count > 0:
            self.stdout.write(self.style.WARNING(f'Found {count} phone(s) with empty IDs'))
            
            # Display them
            for phone in invalid_phones:
                self.stdout.write(f'  - {phone.brand} {phone.model}')
            
            # Delete them
            invalid_phones.delete()
            self.stdout.write(self.style.SUCCESS(f'Successfully deleted {count} invalid phone(s)'))
        else:
            self.stdout.write(self.style.SUCCESS('No invalid phones found'))
