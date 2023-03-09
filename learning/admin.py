from django.contrib import admin
from django.conf import settings
from django.db.models import Count, F
from . import models

# Register your models here.

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user',)
    exclude = ('is_subscribed',)
    list_display = ('first_name', 'last_name', 'user_email','is_subscribed',)
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number')
    list_filter = ('is_subscribed',)
    list_per_page = 10
    list_select_related = ('user',)
    ordering = ('user__first_name', 'user__last_name')

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def user_email(self, obj):
        return obj.user.email
    
    
    def phone_number(self, student):
        return student.user.phone_number
    
    def is_subscribed(self, student):
        return student.user.is_subscribed
    
@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subscription_type', 'price', 'students_count')
    search_fields = ('title',)

    def students_count(self, subscription):
        return subscription.students_count
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(students_count= Count('enrollment'))
    
    students_count.short_description = 'Students Count'

@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    exclude = ('expiration_date',)
    list_display = ('student', 'subscription', 'enrollment_date', 'expiration_date')
    list_per_page = 10
    list_filter = ('subscription',)
    ordering = ('-enrollment_date',)
   

@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'subscription', 'amount', 'payment_date')
    list_per_page = 10
    list_filter = ('subscription',)
    ordering = ('-payment_date',)

@admin.register(models.Passage)
class PassageAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'language')
    search_fields = ('title',)
    list_per_page = 10
    list_filter = ('created_at',)
    ordering = ('created_at',)

@admin.register(models.TypedPassage)
class TypedPassageAdmin(admin.ModelAdmin):
    pass


class StudentFilter(admin.SimpleListFilter):
    title = 'student'
    parameter_name = 'student'

    def lookups(self, request, model_admin):
        students = models.Student.objects.all()
        return [(student.id, str(student)) for student in students]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(student_id=self.value())
        else:
            return queryset
@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'passage', 'subexam', 'test_date')
    list_per_page = 10
    list_filter = ('subexam', StudentFilter)
    ordering = ('-test_date',)



