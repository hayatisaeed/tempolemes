from django.contrib import admin
from accounts.models import StudentProfile


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'national_code', 'phone_number', 'parents_phone_number', 'profile_completed')
    search_fields = ('user__first_name', 'user__last_name', 'national_code', 'phone_number')
    list_filter = ('birthdate_year',)
    ordering = ('user__first_name',)
