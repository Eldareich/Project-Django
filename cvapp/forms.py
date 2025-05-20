from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ('user', 'name', 'resume_templates')

        labels = {
            'first_name': 'First Name',
            'surname': 'Surname',
            'profession': 'Job Title',
            'phone': 'Phone Number',
            'email': 'Email Address',
            'locality': 'Locality',
            'city': 'City',
            'Pin_code': 'Postal Code (Kazpost)',
            'linkedin_link': 'LinkedIn',
            'github_link': 'GitHub',  # ✅ исправлено
            'about': 'About You',     # ✅ исправлено
            'degree': 'Degree',
            'school_name': 'School Name',
            'school_location': 'School Location',
            'College': 'College Name',
            'project': 'Projects',
            'university': 'University',
            'work_experience': 'Work Experience',  # ✅ исправлено
            'skills': 'Skills',
            'interest': 'Interests',  # ✅ исправлено
            'profile_image': 'Profile Photo',
            'certificate': 'Certificates'
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your First Name'}),
            'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Your Last Name'}),
            'profession': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Software Developer'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., +7'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Samal District'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Almaty'}),
            'Pin_code': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g., 050000'}),
            'linkedin_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g., https://linkedin.com/in/username'}),
            'github_link': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g., https://github.com/username'}),  # ✅
            'about': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a short summary about yourself'}),  # ✅
            'school_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., NIS Qyzylorda'}),
            'school_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Qyzylorda'}),
            'College': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Korkyt Ata College'}),
            'degree': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BSc in Computer Science'}),
            'university': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IITU'}),
            'project': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'List your projects'}),
            'work_experience': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Summarize your work experience'}),  # ✅
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, Django, SQL, Git'}),
            'interest': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'e.g., CS2, Volleyball, DOTA2'}),  # ✅
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'certificate': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., IELTS, AWS Certified, Coursera'}),
        }
