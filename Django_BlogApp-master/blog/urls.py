from django.urls import path
from . import views
from django.urls import path
# from .views import BlogDetailView

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    # path('create/', views.create_blog_entry, name='blog-create'),
    # path('blog/<int:post_id>/delete/', views.delete_blog_entry, name='blog-delete'),
    # path('blog/<int:post_id>/', views.blog_post, name='blog-post'),
    # path('blog/<int:pk>/', views.blog_detail, name='blog-detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     # ...
#     path('blog/<int:post_id>/delete/', views.delete_blog_entry, name='blog-delete'),
# ]
