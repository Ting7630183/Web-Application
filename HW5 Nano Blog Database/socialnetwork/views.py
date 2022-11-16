# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone

from socialnetwork.forms import LoginForm, RegisterForm, ProfileForm
from socialnetwork.models import *
from socialnetwork.models import Profile


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
    
    new_profile = Profile(user=request.user)
    new_profile.save()
    return redirect(reverse('global_stream'))

@login_required
def global_stream_action(request):
    context = {}
    if request.method == 'GET':
        print("enter get method")
        return render(request, 'socialnetwork/global_stream.html', {'form': Post.objects.all().order_by('-creation_time')})

    # Adds the new item to the database if the request parameter is present
    if 'test' not in request.POST or not request.POST['test']:
        context['error'] = 'You must enter an item to add.'
        context['form'] = Post.objects.all()
        return render(request, 'socialnetwork/global_stream.html',  context)

    new_post = Post(text=request.POST['test'], user=request.user, creation_time=timezone.now())
    new_post.save()
    return render(request, 'socialnetwork/global_stream.html', {'form': Post.objects.all().order_by('-creation_time')})


@login_required
def get_photo(request, id):
    item = get_object_or_404(Profile, id=id)
    print('Picture #{} fetched from db: {} (type={})'.format(id, item.picture, type(item.picture)))

    # Maybe we don't need this check as form validation requires a picture be uploaded.
    # But someone could have delete the picture leaving the DB with a bad references.
    if not item.picture:
        raise Http404

    return HttpResponse(item.picture, content_type=item.content_type)


@login_required
def my_profile_action(request):
    item = request.user.profile
    
    context = {}
    if request.method == 'GET':
        print("in the get request")
        context = {'items': request.user.profile,
                    'form': ProfileForm(initial = {'bio': request.user.profile.bio})}
        return render(request, 'socialnetwork/my_profile.html', context)
    
    form = ProfileForm(request.POST, request.FILES)

    if not form.is_valid():
        context = {'profile': request.user.profile,'form':form }
        return render(request, 'socialnetwork/my_profile.html', context)
    
    print("in the post branch")
    pic = form.cleaned_data['picture']
    print('Uploaded picture: {} (type={})'.format(pic, type(pic)))

    item.picture = pic

    item.content_type = pic.content_type
    item.bio = form.cleaned_data['bio']
    item.save()

    context = {
        'items': request.user.profile,
        'form': ProfileForm(initial={'bio': request.user.profile.bio})
    }
    return render(request, 'socialnetwork/my_profile.html', context)


def unfollow(request, id):
    user_to_unfollow = get_object_or_404(User, id=id)
    request.user.profile.following.remove(user_to_unfollow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other_profile.html', {'profile': user_to_unfollow.profile})

def follow(request, id):
    user_to_follow = get_object_or_404(User, id=id)
    request.user.profile.following.add(user_to_follow)
    request.user.profile.save()
    return render(request, 'socialnetwork/other_profile.html', {'profile': user_to_follow.profile})


@login_required
def other_profile_action(request, id):
    print("come into other profile")
    user = get_object_or_404(User, id=id)
    return render(request,'socialnetwork/other_profile.html', {'profile':user.profile})

@login_required
def follower_stream_action(request):
    context = {}
    if request.method == 'GET':
        print("enter get method")
        return render(request, 'socialnetwork/follower_stream.html', {'form': Post.objects.all().order_by('-creation_time')})

    
def logout_action(request):
    logout(request)
    return redirect(reverse('login'))
