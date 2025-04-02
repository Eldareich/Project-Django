from django.db import models
class Resume(models.Model):
    full_name = models.CharField(max_length=255)  
    email = models.EmailField(unique=True)  
    phone = models.CharField(max_length=20, blank=True, null=True)  
    summary = models.TextField(blank=True, null=True)  
    skills = models.TextField(blank=True, null=True)  
    experience = models.TextField(blank=True, null=True)
    education = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True) 
    
    def __str__(self):
        return self.full_name
# Create your models here.
