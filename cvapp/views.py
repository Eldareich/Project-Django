from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader, TemplateDoesNotExist

from accounts.models import Account
from cvapp.models import Profile, ResumeTemplate
from cvapp.forms import ProfileForm

import os
import pdfkit
import numpy as np
from sklearn.linear_model import LinearRegression

# wkhtmltopdf path
config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')


def home(request):
    return render(request, 'cvapp/home.html')


def predict(request):
    if request.method == 'POST':
        try:
            experience = float(request.POST.get('experience'))
            X = np.array([[1], [2], [3], [4], [5]])
            y = np.array([30000, 40000, 50000, 60000, 70000])
            model = LinearRegression()
            model.fit(X, y)
            prediction = model.predict(np.array([[experience]]))[0]
            return render(request, 'cvapp/predict.html', {'prediction': round(prediction, 2)})
        except (ValueError, TypeError):
            return HttpResponse("Please enter a valid number.", status=400)
    return render(request, 'cvapp/predict.html')


@method_decorator(login_required, name='dispatch')
class SelectTemplate(View):
    def get(self, request):
        templates = ResumeTemplate.objects.all()
        profile, _ = Profile.objects.get_or_create(user=request.user)
        return render(request, 'cvapp/select_template.html', {
            'templates': templates,
            'profile': profile
        })

    def post(self, request):
        template_id = request.POST.get('template_ids')
        profile, _ = Profile.objects.get_or_create(user=request.user)

        if template_id:
            try:
                selected_template = ResumeTemplate.objects.get(id=template_id)
                profile.resume_templates.set([selected_template])
                profile.save()
                return redirect('accept')
            except ResumeTemplate.DoesNotExist:
                pass

        return render(request, 'cvapp/select_template.html', {
            'templates': ResumeTemplate.objects.all(),
            'profile': profile,
            'error': 'Please select a valid template.'
        })


@method_decorator(login_required, name='dispatch')
class Accept(View):
    def get(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=profile)
        return render(request, 'cvapp/accept.html', {'form': form})

    def post(self, request):
        profile, _ = Profile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            form.save_m2m()
            return redirect('viewing', id=profile.id)
        return render(request, 'cvapp/accept.html', {'form': form})


@login_required
def resume(request, template_id):
    user_profile = get_object_or_404(Profile, pk=template_id)
    skills_list = [skill.strip() for skill in user_profile.skills.split(',')] if user_profile.skills else []

    default_template = 'cvapp/resume.html'
    template_name = default_template

    selected_template = user_profile.resume_templates.first()
    if selected_template and selected_template.template_file:
        try:
            # Путь внутри MEDIA_ROOT
            raw_path = selected_template.template_file.name
            file_name = os.path.basename(raw_path)
            template_name = f'cvapp/{file_name}'
            loader.get_template(template_name)
        except TemplateDoesNotExist:
            print(f"❌ Template {template_name} not found. Using default.")
            template_name = default_template

    profile_image_path = None
    if user_profile.profile_image and os.path.exists(user_profile.profile_image.path):
        fixed_path = user_profile.profile_image.path.replace("\\", "/")
        profile_image_path = f'file:///{fixed_path}'


    context = {
        'user_profile': user_profile,
        'skills_list': skills_list,
        'profile_image_path': profile_image_path
    }

    try:
        html = loader.render_to_string(template_name, context)
    except Exception as e:
        print(f"❌ Rendering failed: {e}")
        html = loader.render_to_string(default_template, context)

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
        'enable-local-file-access': ''
    }

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user_profile.first_name}_resume.pdf"'
    return response


def list(request):
    users = Profile.objects.all()
    return render(request, 'cvapp/list.html', {'UserCV': users})


@login_required
def UserDetail(request, id):
    account = get_object_or_404(Account, email=request.user.email)
    visitor = get_object_or_404(Profile, pk=id)
    if account.email == visitor.user.email or account.is_staff:
        return render(request, 'cvapp/Individual-User.html', {'Visitor': visitor})
    return render(request, 'cvapp/unauthorized_access.html')


def update_form(request, id):
    profile = get_object_or_404(Profile, pk=id)
    form = ProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('viewing', id=id)
    return render(request, 'cvapp/accept.html', {'form': form, 'review': profile})


def delete_form(request, id):
    profile = get_object_or_404(Profile, pk=id)
    if request.method == 'POST':
        profile.delete()
        return redirect('list')
    return render(request, 'cvapp/deletecv.html', {'review': profile})

def resume_template_10(request):
    return render(request, 'cvapp/resumetemplate10.html')

def resume_template_20(request):
    return render(request, 'cvapp/resumetemplate20.html')

def resume_template_30(request):
    return render(request, 'cvapp/resumetemplate30.html')
