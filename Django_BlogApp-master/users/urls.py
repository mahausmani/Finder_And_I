from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post, name='post'), 
    path('', views.home, name='home'),
    path('about',views.about, name='about'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('search/', views.search, name='search'),
    path('user/<str:username>/', views.user_profile, name='user_profile'),
    path('friend-requests/', views.friend_requests, name='friend_requests'),
    path('send-friend-request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('your-friends/', views.your_friends, name='your_friends'),
    path('accept-friend-request/<int:request_id>/', views.accept_friend_request, name='accept_friend_request'),
    path('reject-friend-request/<int:request_id>/', views.reject_friend_request, name='reject_friend_request'),
    path('unfriend/<str:username>/', views.unfriend, name='unfriend')

]
