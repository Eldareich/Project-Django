import logging
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterationForm, ProfileForm
from .models import Account, UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

# Логгер для отслеживания ошибок
logger = logging.getLogger(__name__)

# Register view
def register(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(
                first_name=first_name, last_name=last_name, email=email, username=username, password=password)
            user.phone_number = phone_number
            user.save()

            # User activation email
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])

            try:
                send_email.send()  # Отправка email
            except Exception as e:
                logger.error(f"Error sending email to {email}: {e}")  # Логируем ошибку
                messages.error(request, 'There was an error sending the activation email.')
                return redirect('register')  # Перенаправление при ошибке

            messages.success(request, 'Please verify your email to activate your account.')
            return redirect('/accounts/login/?command=verification&email=' + email)
    else:
        form = RegisterationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


# Login view
def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password.')
            return redirect('login')

    return render(request, 'accounts/login_user.html')


# Logout view
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, 'You have logged out successfully.')
    return redirect('login')


# Account activation view
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated successfully!')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link!')
        return redirect('register')


# Forgot password view
def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email=email)

            current_site = get_current_site(request)
            mail_subject = 'Reset your password'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])

            try:
                send_email.send()  # Отправка email
            except Exception as e:
                logger.error(f"Error sending reset password email to {email}: {e}")
                messages.error(request, 'There was an error sending the reset password email.')
                return redirect('forgotPassword')

            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist with this email address.')
            return redirect('forgotPassword')

    return render(request, 'accounts/forgotPassword.html')


# Password reset validation view
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password.')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired or is invalid.')
        return redirect('login')


# Password reset view
def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been successfully reset!')
            return redirect('login')
        else:
            messages.error(request, 'Passwords do not match.')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


# Profile view
@login_required
def profile_view(request, username=None):
    if username:
        account = get_object_or_404(Account, username=username)
    else:
        account = request.user

    try:
        profile = account.userprofile
    except UserProfile.DoesNotExist:
        raise Http404("Profile does not exist")

    return render(request, 'accounts/profile.html', {'profile': profile})


# Profile edit view
@login_required
def profile_edit_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        raise Http404("Profile does not exist")

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')

    if request.path == reverse('profile-registercreate'):
        template = 'accounts/profile_registercreate.html'
    else:
        template = 'accounts/profile_edit.html'

    return render(request, template, {'form': form})


# Profile delete view
@login_required
def profile_delete_view(request):
    user = request.user

    if request.method == 'POST':
        logout(request)
        user.delete()
        messages.success(request, 'Your account has been deleted successfully.')
        return redirect('home')

    return render(request, 'accounts/profile_delete.html')
