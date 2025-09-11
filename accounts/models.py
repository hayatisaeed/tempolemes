from django.db import models


class StudentProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='student_profile')
    national_code = models.CharField(max_length=10, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    bio = models.TextField(blank=True)
    birthdate_day = models.CharField(max_length=2, null=True, blank=True)
    birthdate_month = models.CharField(max_length=2, null=True, blank=True)
    birthdate_year = models.CharField(max_length=4, null=True, blank=True)

    @property
    def birth_date(self):
        if self.birthdate_day and self.birthdate_month and self.birthdate_year:
            return f"{self.birthdate_year}/{self.birthdate_month.zfill(2)}/{self.birthdate_day.zfill(2)}"
        return None
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.national_code}"
