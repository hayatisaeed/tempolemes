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
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='exam_participations')

    answer_file = models.FileField(upload_to='exam_answers/', blank=True, null=True)
    
    start_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.exam}"
    
    class Meta:
        unique_together = ('exam', 'student')


class ExamResult(models.Model):
    participation = models.OneToOneField(ExamParticipation, on_delete=models.CASCADE, related_name='result')
    graded_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True, blank=True)
    grade_date = models.DateTimeField(auto_now_add=True)

    score = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Result for {self.participation}"
