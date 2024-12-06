from django.db import models

class SpyCat(models.Model):
    name = models.CharField(max_length=255)
    experience = models.PositiveIntegerField()
    breed = models.CharField(max_length=255)
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name