from django.db import models
from accounts.models import Account

class ResumeTemplate(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='template_images/', null=True, blank=True)
    template_file = models.FileField(upload_to='templates/', null=True, blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    resume_templates = models.ManyToManyField(ResumeTemplate, blank=True)

    first_name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    profession = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)

    locality = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    pin_code = models.CharField(max_length=10, null=True, blank=True)
    linkedin_link = models.URLField(max_length=300, blank=True)
    github_link = models.URLField(max_length=300, blank=True)
    about = models.TextField(max_length=1000, null=True, blank=True)

    school_name = models.CharField(max_length=200, null=True, blank=True)
    school_location = models.CharField(max_length=200, null=True, blank=True)
    college = models.CharField(max_length=200, null=True, blank=True)
    degree = models.CharField(max_length=100, null=True, blank=True)
    university = models.CharField(max_length=300, null=True, blank=True)
    project = models.TextField(max_length=1000, null=True, blank=True)
    work_experience = models.TextField(max_length=1000, null=True, blank=True)
    skills = models.TextField(max_length=1000, null=True, blank=True)
    interest = models.CharField(max_length=500, blank=True, null=True)

    profile_image = models.ImageField(
        upload_to='profilepic/',
        default='profilepic/default.jpg',
        blank=True,
        null=True
    )

    certificate = models.TextField(max_length=1000, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.surname} Profile'
