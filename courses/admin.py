from django.contrib import admin
from .models import Course, CourseEnrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(CourseEnrollment)
class CourseEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('course', 'student', 'enrollment_date')
    search_fields = ('course__name',)
    list_filter = ('enrollment_date',)
    readonly_fields = ('enrollment_date',)
