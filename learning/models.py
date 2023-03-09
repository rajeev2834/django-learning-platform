from django.db import models
from django.conf import settings
from django.utils import timezone

from exams.models import SubExam

# Create your models here.

class Student(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=10)
    is_subscribed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Subscription(models.Model):

    subscription_type_choices = [
        ('Free', 'Free'),
        ('Weekly', 'Weekly'),
        ('Bi-Weekly', 'Bi-Weekly'),
        ('Monthly', 'Monthly'),
        ('Yearly', 'Yearly'),
    ]

    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    subscription_type = models.CharField(max_length=255, choices=subscription_type_choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def get_duration(self):
        duration_choices = {
            'Free': 0,
            'Weekly': 7,
            'Bi-Weekly': 15,
            'Monthly': 30,
            'Yearly': 365,
            # Add more duration choices as needed
        }
        return duration_choices.get(self.subscription_type)

class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    enrollment_date = models.DateField(auto_now_add=True)
    expiration_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.expiration_date = self.get_expiration_date()
        super(Enrollment, self).save(*args, **kwargs)

        if self.expiration_date and self.expiration_date > timezone.now().date():
            Student.objects.filter(id=self.student.id).update(is_subscribed=True)

    def get_expiration_date(self):
        duration = self.subscription.get_duration()
        expiration_date = self.enrollment_date + timezone.timedelta(days=duration)
        return expiration_date
    
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=255)
    utr_number = models.CharField(max_length = 50, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length = 50, null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class Passage(models.Model):

    LANGUAGE_ENGLISH = 'EN'
    LANGUAGE_HINDI = 'HI'

    LANGUAGE_CHOICES = (
        (LANGUAGE_ENGLISH, 'English'),
        (LANGUAGE_HINDI, 'Hindi'),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    passage_text = models.TextField()
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default=LANGUAGE_ENGLISH)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class TypedPassage(models.Model):

    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subexam = models.ForeignKey(SubExam, on_delete=models.CASCADE) 
    typed_passage_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

class Result(models.Model):

    passage = models.ForeignKey(Passage, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subexam = models.ForeignKey(SubExam, on_delete=models.CASCADE)
    typed_passage = models.ForeignKey(TypedPassage, on_delete=models.CASCADE)
    wpm = models.IntegerField()
    accuracy = models.DecimalField(max_digits=5, decimal_places=2)
    net_speed = models.DecimalField(max_digits=5, decimal_places=2)
    gross_speed = models.DecimalField(max_digits=5, decimal_places=2)
    total_errors = models.IntegerField()
    total_marks = models.DecimalField(max_digits=5, decimal_places=2)
    test_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)