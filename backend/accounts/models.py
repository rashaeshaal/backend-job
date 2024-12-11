from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from adminapp.models import JobPosting 

# Create your models here.


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return f"{self.name} ({self.state.name})"

class UserProfile(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]  

    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    terms_and_conditions = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

    def clean(self):
        if self.date_of_birth and (timezone.now().date() - self.date_of_birth).days < 18 * 365:
            raise ValidationError("You must be at least 18 years old.")

class JobApplication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_applications')
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE)  
    resume = models.FileField(upload_to='job_applications/resumes/') 
    status = models.CharField(max_length=20, choices=[('Applied', 'Applied'), ('Interview', 'Interview'), ('Hired', 'Hired')], default='Applied')
    applied_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} applied for {self.job_posting.job_title}"