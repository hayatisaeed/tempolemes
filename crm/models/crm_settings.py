from django.db import models
from courses.models import Course, CourseEnrollment
from django.contrib.contenttypes.models import ContentType
from exams.models import Exam, ExamParticipation, ExamResult
from crm.models import DealStage


class Setting(models.Model):
    related_changed_model = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='settings_for_changed_models', null=True, blank=True)
    crud_choices = [
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
    ]
    crud_type = models.CharField(max_length=10, choices=crud_choices)

    new_deal_stage = models.ForeignKey(DealStage, on_delete=models.DO_NOTHING, related_name='settings_for_changed_deals', null=True, blank=True, help_text="Select the deal stage for new deals created.")
    
    def __str__(self):
        return f"Setting for: {self.related_changed_model} - {self.crud_type}"

    class Meta:
        verbose_name = "Setting"
        verbose_name_plural = "Settings"
        unique_together = ('related_changed_model', 'crud_type')