from django.db import models

class Customer(models.Model):
    related_student_profile = models.OneToOneField('accounts.StudentProfile', on_delete=models.CASCADE, null=True, blank=True, related_name='customer')
    related_user = models.OneToOneField('auth.User', on_delete=models.CASCADE, null=True, blank=True)

    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)

    national_code = models.CharField(max_length=10, unique=True, null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    parents_phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    

class CustomerNote(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notes')
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Note for {self.customer.first_name} {self.customer.last_name} at {self.created_at}"
    