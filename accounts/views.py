from django.shortcuts import render, redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            print(email)
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            print(password)
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username,
                                               email=email, password=password)
            user.phone_number = phone_number
            user.save()
            messages.success(request, 'Registration Successful!')
            print(email)
            print(password)
            redirect('user-register')

    else:
        form = RegistrationForm()

    context = {
        'form': form,
    }
    return render(request, 'accounts/register.html', context)


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        print(email)
        password = request.POST['password']
        print(password)
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            #messages.success(request,)
            return redirect('core-home')
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
