from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.post, name='post'), 
    path('', views.home, name='home'),
    path('/about',views.about, name = 'about'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    
]
