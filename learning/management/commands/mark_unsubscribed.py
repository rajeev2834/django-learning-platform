from django.core.management.base import BaseCommand
from django.db.models import F
from datetime import date
from learning.models import Student, Enrollment

class Command(BaseCommand):
    help = 'Marks students as unsubscribed whose enrollment has expired'

    def handle(self, *args, **options):
        unsubscribed_student_ids = Student.objects.filter(
            enrollment__expiration_date__lt=date.today(),
            is_subscribed=True
        ).values_list('id', flat=True)

        Student.objects.filter(id__in=unsubscribed_student_ids).update(is_subscribed=False)

        self.stdout.write(self.style.SUCCESS(f'Successfully marked {len(unsubscribed_student_ids)} students as unsubscribed'))