from django.contrib import admin
from django.conf import settings
from . import models

# Register your models here.

@admin.register(models.Student)
class StudentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('user',)
    list_display = ('first_name', 'last_name', 'user_email', 'phone_number')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'phone_number')
    list_per_page = 10
    list_editable = ('phone_number',)
    list_filter = ('created_at', 'updated_at')
    list_select_related = ('user',)
    ordering = ('user__first_name', 'user__last_name')

    def first_name(self, obj):
        return obj.user.first_name
    
    def last_name(self, obj):
        return obj.user.last_name
    
    def user_email(self, obj):
        return obj.user.email
    
@admin.register(models.Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('title', 'subscription_type', 'price')
    search_fields = ('title',)

@admin.register(models.Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
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

@admin.register(models.Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('student', 'passage', 'subexam', 'test_date')
    list_per_page = 10
    list_filter = ('subexam',)
    ordering = ('-test_date',)



