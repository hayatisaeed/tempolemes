from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import StudentProfile
from crm.models import Customer

@receiver(post_save, sender=User)
def create_student_profile(sender, instance, created, **kwargs):
    if created:
        StudentProfile.objects.create(user=instance)

@receiver(post_save, sender=StudentProfile)
def create_customer_for_student_profile(sender, instance, created, **kwargs):
    if created:
        if instance.profile_completed:
            Customer.objects.get_or_create(
                related_student_profile=instance,
                related_user=instance.user,
                defaults={
                    'first_name': instance.first_name,
                    'last_name': instance.last_name,
                    'national_code': instance.national_code,
                    'phone_number': instance.phone_number,
                    'parents_phone_number': instance.parents_phone_number,
                    'address': instance.address,
                }
            )
