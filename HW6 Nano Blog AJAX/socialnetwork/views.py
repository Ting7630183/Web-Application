# Create your views here.
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponse, Http404
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from socialnetwork.forms import LoginForm, RegisterForm, ProfileForm
from socialnetwork.models import *
from socialnetwork.models import Profile
from socialnetwork.models import Comment
from django.views.decorators.csrf import ensure_csrf_cookie
import json


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
    
def get_global(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    response_data = []

    for model_item in Post.objects.all():
        comments = []
        for comment in model_item.comment_set.all().order_by('creation_time'):
            my_comment = {
                'id': comment.id,
                'text': comment.text,
                'creator_first_name': comment.creator.first_name,
                'creator_last_name':comment.creator.last_name,
                'creator_id':comment.creator.id,
                # 'creation_time':parse_datetime(str(comment.creation_time)).isoformat(),
                'creation_time':str(comment.creation_time),
                'post_id':comment.post.id
            }
            comments.append(my_comment)

        my_item = {
            'id': model_item.id,
            'text': model_item.text,
            'user_first_name': model_item.user.first_name,
            'user_last_name':model_item.user.last_name,
            'user_id':model_item.user.id,
            # 'creation_time':parse_datetime(str(model_item.creation_time)).isoformat(),
            'creation_time':str(model_item.creation_time),
            'comment': comments
        }
        # print(my_item)
        response_data.append(my_item)
    
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')


def get_follower(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)

    response_data = []

    for model_item in Post.objects.all():
        if model_item.user in request.user.profile.following.all():
            comments = []
            for comment in model_item.comment_set.all().order_by('creation_time'):
                my_comment = {
                    'id': comment.id,
                    'text': comment.text,
                    'creator_first_name': comment.creator.first_name,
                    'creator_last_name':comment.creator.last_name,
                    'creator_id':comment.creator.id,
                    # 'creation_time':parse_datetime(str(comment.creation_time)).isoformat(),
                    'creation_time':str(comment.creation_time),
                    'post_id':comment.post.id
                }
                comments.append(my_comment)

            my_item = {
                'id': model_item.id,
                'text': model_item.text,
                'user_first_name': model_item.user.first_name,
                'user_last_name':model_item.user.last_name,
                'user_id':model_item.user.id,
                # 'creation_time':parse_datetime(str(model_item.creation_time)).isoformat(),
                'creation_time':str(model_item.creation_time),
                'comment': comments
            }
            # print(my_item)
            response_data.append(my_item)
    
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')


def add_comment(request):
    if not request.user.id:
        return _my_json_error_response("You must be logged in to do this operation", status=401)
    
    if request.method != 'POST':
        return _my_json_error_response("You must use a POST request for this operation", status=405)

    if not 'comment_text' in request.POST or not request.POST['comment_text']:
        return _my_json_error_response("You must enter an item to add.", status=400)
    
    if not 'post_id' in request.POST or not request.POST['post_id']:
        return _my_json_error_response("You must enter an item to add.", status=400)
    
    try:
        val = int(request.POST['post_id'])
    except Exception as e:
        return _my_json_error_response("You must enter an item to add.", status=400)
    
    post_id = request.POST['post_id']
    try:
        val = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return _my_json_error_response("You must enter an item to add.", status=400)
   

    post = Post.objects.get(id=post_id)
    new_item = Comment(text=request.POST['comment_text'], creator=request.user, creation_time=timezone.now(), post=post)
    new_item.save()
    post_after = Post.objects.get(id=post_id)

    response_data = []
    comments = []
    my_comment = {
                    'id': new_item.id,
                    'text': new_item.text,
                    'creator_first_name': new_item.creator.first_name,
                    'creator_last_name':new_item.creator.last_name,
                    'creator_id':new_item.creator.id,
                    # 'creation_time':parse_datetime(str(comment.creation_time)).isoformat(),
                    'creation_time':str(new_item.creation_time),
                    'post_id':new_item.post.id
                }
    comments.append(my_comment)

    my_item = {
                'id': post_after.id,
                'text': post_after.text,
                'user_first_name': post_after.user.first_name,
                'user_last_name':post_after.user.last_name,
                'user_id':post_after.user.id,
                # 'creation_time':parse_datetime(str(model_item.creation_time)).isoformat(),
                'creation_time':str(post_after.creation_time),
                'comment': comments
            }
    response_data.append(my_item)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type='application/json')

def _my_json_error_response(message, status=200):
    # You can create your JSON by constructing the string representation yourself (or just use json.dumps)
    response_json = '{ "error": "' + message + '" }'
    return HttpResponse(response_json, content_type='application/json', status=status)

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
