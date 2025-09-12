from django.db import models
from accounts.validators import validate_national_code, validate_phone_number


class StudentProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, related_name='student_profile')
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    national_code = models.CharField(max_length=10, unique=True, validators=[validate_national_code], null=True, blank=True)
    phone_number = models.CharField(max_length=11, unique=True, validators=[validate_phone_number], null=True, blank=True)
    parents_phone_number = models.CharField(max_length=11, validators=[validate_phone_number], null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
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
        return f"{self.first_name} {self.last_name}"
    
    @property
    def profile_completed(self):
        return all([self.first_name, self.last_name, self.national_code, self.phone_number, self.birth_date, self.parents_phone_number])
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} - {self.national_code}"
