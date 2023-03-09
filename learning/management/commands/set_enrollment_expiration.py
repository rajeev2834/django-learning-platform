from django.core.management.base import BaseCommand
from learning.models import Enrollment

class Command(BaseCommand):
    help = 'Set the expiration date for all enrollments'

    def handle(self, *args, **options):
        enrollments = Enrollment.objects.all()
        for enrollment in enrollments:
            if not enrollment.expiration_date:
                expiration_date = enrollment.get_expiration_date()
                enrollment.expiration_date = expiration_date
                enrollment.save()
        self.stdout.write(self.style.SUCCESS('Successfully set expiration dates for all enrollments'))
