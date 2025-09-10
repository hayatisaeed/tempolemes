from django.db import models

class Pipeline(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class DealStage(models.Model):
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)
    order = models.IntegerField()

    def __str__(self):
        return self.name
    

class Deal(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    stage = models.ForeignKey(DealStage, on_delete=models.CASCADE, related_name='deals')

    related_product = models.ForeignKey('crm.Product', on_delete=models.CASCADE, null=True, blank=True)
    related_customer = models.ForeignKey('crm.Customer', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.title:
            self.title = f"Deal for {self.related_customer} - {self.related_product}"
        super().save(*args, **kwargs)
