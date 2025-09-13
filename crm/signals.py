from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import StudentProfile
from courses.models import Course, CourseEnrollment
from exams.models import Exam, ExamParticipation, ExamResult
from crm.models import Customer, CustomerNote, Deal, DealStage, Setting, Product, DealNote


@receiver(post_save, sender=CourseEnrollment)
def create_deal_for_course_enrollment(sender, instance, created, **kwargs):
    if created:
        print("line13")
        setting = Setting.objects.filter(
            related_changed_model__model=CourseEnrollment._meta.model_name,
            crud_type='create',
            new_deal_stage__isnull=False
        ).first()
        product = Product.objects.filter(related_course=instance.course).first()
        if setting:
            print("line21")
            deal, deal_created = Deal.objects.get_or_create(
                related_customer=instance.student.student_profile.customer,
                related_product=product,
                defaults={
                    'stage':setting.new_deal_stage
                }
            )
            print("deal created")
            DealNote.objects.create(
                deal = deal,
                note = f"Deal {deal.id} created for Course Enrollment ID {instance.id}."
            )
            CustomerNote.objects.create(
                customer=instance.student.student_profile.customer,
                note=f"New deal created for Course Enrollment ID {instance.id}. Deal ID: {deal.id}."
            )
    else:
        setting = Setting.objects.filter(
            related_changed_model__model=CourseEnrollment._meta.model_name,
            crud_type='update',
            new_deal_stage__isnull=False
        ).first()
        if setting:
            deals = Deal.objects.filter(
                customer=instance.student.student_profile.customer,
                product__related_course=instance.course
            )
            for deal in deals:
                deal.stage = setting.new_deal_stage
                deal.save()
                DealNote.objects.create(
                    deal = deal,
                    note = f"Deal stage updated for Course Enrollment ID {instance.id}."
                )
                CustomerNote.objects.create(
                    customer=instance.student.student_profile.customer,
                    note=f"Deal stage updated to {setting.new_deal_state} for Deal ID {deal.id}."
                )

@receiver(post_save, sender=ExamParticipation)
def create_deal_for_exam_participation(sender, instance, created, **kwargs):
    if created:
        setting = Setting.objects.filter(
            related_changed_model__model=ExamParticipation._meta.model_name,
            crud_type='create',
            new_deal_stage__isnull=False
        ).first()
        product = Product.objects.filter(related_course=instance.exam.course).first()
        if setting:
            deal = Deal.objects.create(
                customer=instance.student.student_profile.customer,
                product=product,
                stage=setting.new_deal_stage,
            )
            DealNote.objects.create(
                deal = deal,
                note = f"Deal {deal.id} created for Exam Participation ID {instance.id}."
            )
            CustomerNote.objects.create(
                customer=instance.student_profile.customer,
                note=f"New deal created for Exam Participation ID {instance.id}. Deal ID: {deal.id}."
            )
    else:
        setting = Setting.objects.filter(
            related_changed_model__model=ExamParticipation._meta.model_name,
            crud_type='update',
            new_deal_stage__isnull=False
        ).first()
        if setting:
            deals = Deal.objects.filter(
                customer=instance.student.student_profile.customer,
                product__related_course=instance.exam.related_course
            )
            for deal in deals:
                deal.deal_stage = setting.new_deal_stage
                deal.save()
                DealNote.objects.create(
                    deal = deal,
                    note = f"Deal stage updated for Exam Participation ID {instance.id}."
                )
                CustomerNote.objects.create(
                    customer=instance.student.student_profile.customer,
                    note=f"Deal stage updated to {setting.new_deal_state} for Deal ID {deal.id}."
                )

@receiver(post_save, sender=ExamResult)
def create_deal_for_exam_result(sender, instance, created, **kwargs):
    if created:
        setting = Setting.objects.filter(
            related_changed_model__model=ExamResult._meta.model_name,
            crud_type='create',
            new_deal_stage__isnull=False
        ).first()
        product = Product.objects.filter(related_course=instance.participation.exam.related_course).first()
        if setting:
            deal = Deal.objects.create(
                customer=instance.participation.student.student_profile.customer,
                product=product,
                deal_stage=setting.new_deal_stage,
            )
            DealNote.objects.create(
                deal = deal,
                note = f"Deal {deal.id} created for Exam Result ID {instance.id}."
            )
            CustomerNote.objects.create(
                customer=instance.participation.student.student_profile.customer,
                note=f"New deal created for Exam Result ID {instance.id}. Deal ID: {deal.id}."
            )
    else:
        setting = Setting.objects.filter(
            related_changed_model__model=ExamResult._meta.model_name,
            crud_type='update',
            new_deal_stage__isnull=False
        ).first()
        if setting:
            deals = Deal.objects.filter(
                customer=instance.participation.student.student_profile.customer,
                product__related_course=instance.participation.exam.course
            )
            for deal in deals:
                deal.deal_stage = setting.new_deal_stage
                deal.save()
                DealNote.objects.create(
                    deal = deal,
                    note = f"Deal stage updated for Exam Result ID {instance.id}."
                )
                CustomerNote.objects.create(
                    customer=instance.participation.student.student_profile.customer,
                    note=f"Deal stage updated to {setting.new_deal_state} for Deal ID {deal.id}."
                )
