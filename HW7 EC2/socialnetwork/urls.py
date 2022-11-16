from django.urls import path
from socialnetwork import views

urlpatterns = [
    path('global_stream', views.global_stream_action, name='global_stream'),
    path('login', views.login_action, name='login'),
    path('register', views.register_action, name='register'),
    path('follower_stream', views.follower_stream_action, name='follower_stream'),
    path('logout', views.logout_action, name='logout'),
    path('my_profile', views.my_profile_action, name='my_profile'),
    path('other_profile/<int:id>', views.other_profile_action, name='other_profile'),
    path('photo/<int:id>', views.get_photo, name='photo'),
    path('unfollow/<int:id>', views.unfollow, name='unfollow'),
    path('follow/<int:id>', views.follow, name='follow'),
    path('get-global', views.get_global), 
    path('get-follower', views.get_follower), 
    path('add-comment', views.add_comment), 
]
