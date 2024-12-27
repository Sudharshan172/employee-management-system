from django.db import models
from django.core.validators import MinValueValidator

class Employee(models.Model):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    salary = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    bonus = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    phone = models.CharField(max_length=15, default='', null=False)
    department = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100, default='Not Assigned')
    hire_date = models.DateField(null=False)
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"

    class Meta:
        db_table = 'employee_details'
