
# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm

def login_action(request):
    context = {}

    if request.user.is_authenticated:
        return redirect(reverse('global_stream'))

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = LoginForm()
        return render(request, 'socialnetwork/login.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = LoginForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/login.html', context)

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['password'])

    login(request, new_user)
    return redirect(reverse('global_stream'))

def register_action(request):
    context = {}

    # Just display the registration form if this is a GET request.
    if request.method == 'GET':
        context['form'] = RegisterForm()
        return render(request, 'socialnetwork/register.html', context)

    # Creates a bound form from the request POST parameters and makes the 
    # form available in the request context dictionary.
    form = RegisterForm(request.POST)
    context['form'] = form

    # Validates the form.
    if not form.is_valid():
        return render(request, 'socialnetwork/register.html', context)

    # At this point, the form data is valid.  Register and login the user.
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['confirm_password'],
                                        email=form.cleaned_data['email'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'])
    new_user.save()

    new_user = authenticate(username=form.cleaned_data['username'],
                            password=form.cleaned_data['confirm_password'])

    login(request, new_user)
    return redirect(reverse('global_stream'))

@login_required
def global_stream_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'socialnetwork/global_stream.html', context)

@login_required
def follower_stream_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'socialnetwork/follower_stream.html', context)

@login_required
def my_profile_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'socialnetwork/my_profile.html', context)

@login_required
def other_profile_action(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'socialnetwork/other_profile.html', context)


def logout_action(request):
    logout(request)
    return redirect(reverse('login'))
