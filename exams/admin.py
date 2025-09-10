from django.contrib import admin
from exams.models import Exam, ExamParticipation


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('title', 'related_course__name', 'duration_minutes', 'total_marks', 'start_date', 'end_date')
    search_fields = ('title', 'related_course__name')
    list_filter = ('related_course__name',)

@admin.register(ExamParticipation)
class ExamParticipationAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'score', 'completed')
    search_fields = ('exam__title', 'student__user__username')
    list_filter = ('completed',)
