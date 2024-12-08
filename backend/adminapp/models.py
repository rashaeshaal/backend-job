from django.db import models
from django.contrib.auth.models import User


class Industry(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=100)
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='roles')

    def __str__(self):
        return f"{self.name} ({self.industry.name})"

class JobPosting(models.Model):
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    salary_min = models.DecimalField(max_digits=10, decimal_places=2)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2)
    job_industry = models.ForeignKey(Industry, on_delete=models.CASCADE)
    job_role = models.ForeignKey(Role, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.job_title

    def save(self, *args, **kwargs):
        if self.salary_min > self.salary_max:
            raise ValueError("Minimum salary cannot be greater than maximum salary.")
        super().save(*args, **kwargs)

