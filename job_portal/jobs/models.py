from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('employer', 'Employer'),
        ('applicant', 'Applicant'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Job(models.Model):
    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} at {self.company_name}"

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-applied_at']
        unique_together = ['job', 'applicant']  # Prevent duplicate applications
    
    def __str__(self):
        return f"{self.applicant.username} applied for {self.job.title}"

