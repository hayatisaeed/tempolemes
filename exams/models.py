from django.db import models


class Exam(models.Model):
    title = models.CharField(max_length=200)
    related_course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, related_name='exams')
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    duration_minutes = models.IntegerField()
    total_marks = models.DecimalField(max_digits=10, decimal_places=2)

    questions_file = models.FileField(upload_to='exam_questions/', blank=True, null=True)

    def __str__(self):
        return self.title


class ExamParticipation(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='participations')
    student = models.ForeignKey('accounts.StudentProfile', on_delete=models.CASCADE, related_name='exam_participations')

    answer_file = models.FileField(upload_to='exam_answers/', blank=True, null=True)
    
    start_date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(blank=True, null=True)

    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.exam}"
    
    class Meta:
        unique_together = ('exam', 'student')
