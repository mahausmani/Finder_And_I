from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CreatePostForm
from .models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    user_posts = Post.objects.filter(author=request.user)
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('profile')
    else:
        form = CreatePostForm()
    context = {
        'user_posts': user_posts,
        'form': form
    }
    return render(request, 'users/profile.html', context)