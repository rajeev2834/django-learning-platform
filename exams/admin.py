from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.


class SubExamInline(admin.StackedInline):
    model = models.SubExam
    extra = 1

@admin.register(models.Exam)
class ExamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'subexams_count')
    inlines = (SubExamInline,)
    search_fields = ('title',)
    list_per_page = 10
    list_filter = ('created_at', 'updated_at')
    ordering = ('created_at',)

    @admin.display(ordering='subexams_count')
    def subexams_count(self, exam):
        reverse_url = (
            reverse('admin:exams_subexam_changelist') +
            '?' +
            urlencode({
                'exam__id': str(exam.id),
            })
        )
        return format_html(f'<a href="{reverse_url}">{exam.subexams_count}</a>')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.annotate(subexams_count=Count('subexam'))
        return qs

@admin.register(models.SubExam)
class SubExamAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ('title', 'slug', 'students_count' , 'exam_title')
    search_fields = ('title',)
    list_per_page = 10
    list_filter = ('exam',)
    list_select_related = ('exam',)
    ordering = ('created_at',)

    @admin.display(ordering='students_count')
    def students_count(self, subexam):
        return subexam.students_count
    
    def exam_title(self, subexam):
        return subexam.exam.title
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(students_count = Count('result')).select_related('exam')