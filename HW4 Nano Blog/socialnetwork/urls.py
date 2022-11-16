from django.urls import path
from socialnetwork import views

urlpatterns = [
    path(' ', views.global_stream_action, name='global_stream'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('follower_stream', views.follower_stream_action, name='follower_stream'),
    path('logout', views.logout_action, name='logout'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('other_profile', views.other_profile_action, name='other_profile'),


    
]
