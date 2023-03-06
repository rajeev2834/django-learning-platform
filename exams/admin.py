from django.contrib import admin
from django.db.models import Count
from . import models

# Register your models here.

@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug',)
    search_fields = ('title',)
    list_per_page = 10
    list_filter = ('created_at', 'updated_at')
    ordering = ('created_at',)

@admin.register(models.SubExam)
class SubExamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'students_count')
    search_fields = ('title',)
    list_per_page = 10
    list_filter = ('created_at', 'updated_at')
    ordering = ('created_at',)

    def students_count(self, subexam):
        return subexam.students_count()
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(students_count = Count('result'))