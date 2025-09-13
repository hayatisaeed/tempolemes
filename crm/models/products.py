from django.db import models
from courses.models import Course

class Product(models.Model):
    name = models.CharField(max_length=100)
    
    related_course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, related_name='products', null=True, blank=True)
    
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name