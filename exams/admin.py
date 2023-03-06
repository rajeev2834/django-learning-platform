from django.contrib import admin
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
    list_display = ('title', 'slug')
    search_fields = ('title',)
    list_per_page = 10
    list_filter = ('created_at', 'updated_at')
    ordering = ('created_at',)