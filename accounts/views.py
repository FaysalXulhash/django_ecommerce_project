from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# account active.
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                               email=email, password=password)
            user.phone_number = phone_number
            user.save()
            # user activation
            current_site = get_current_site(request)
            mail_subject = 'Please active your account'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()

            #messages.success(request, 'Thank you for registration! We have sent verification email,please check it
            # and activate your account.')
            return redirect('/account/login/?command=verification&email='+email)

    else:
        form = RegistrationForm()
    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid login credentials!')
            return redirect('login')
    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out!')
    return redirect('login')
    return render(request, 'accounts/logout.html')

# account activation after register


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! you account has been activate.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link.')
        return redirect('user-register')
    return

@login_required(login_url='login')
def dashboard(request):
    return render(request, 'accounts/dashboard.html')

# send forget password request to email
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)
            # reset password
            current_site = get_current_site(request)
            mail_subject = 'Password change request'
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = email
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            messages.success(request, 'Password reset email hase been sent to your email address')
            return redirect('email_info')
        else:
            messages.error(request, "Account doesn't exist!")
            return redirect('forgot-password')
    return render(request, 'accounts/forgot_password.html')

def email_info(request):
    return render(request, 'accounts/email_info.html')

# check if the forget password request come from validate user
def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link hase been expired!')
        return redirect('login')

# will set the new password for existing user
def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        if password == password2:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successfully. You can log in now with new password')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect('reset_password')
    else:
        return render(request, 'accounts/reset_password.html')
