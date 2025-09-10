from django.db import models

class TaskType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    completed = models.BooleanField(default=False)

    related_customer = models.ForeignKey('crm.Customer', on_delete=models.DO_NOTHING, null=True, blank=True)
    related_deal = models.ForeignKey('crm.Deal', on_delete=models.DO_NOTHING, null=True, blank=True)
    
    task_type = models.ForeignKey(TaskType, on_delete=models.DO_NOTHING, null=True, blank=True)

    assigned_to = models.ForeignKey('auth.User', on_delete=models.DO_NOTHING, null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
