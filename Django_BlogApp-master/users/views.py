from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, CreatePostForm
from .models import Post, Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse


def about(request):
    return render(request, 'users/about.html', {'title':'About'})

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES) # add request.FILES to handle uploaded files
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to log in')
            
            profile = Profile(user=user)
            
            if 'profile_picture' in request.FILES:
                profile.profile_picture = request.FILES['profile_picture']
                
            profile.save() # save the profile object
            
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content:
            post = Post.objects.create(content=content, author=request.user, image=image)
            return redirect('home')
        
@login_required
def profile(request):
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
    
    profile = Profile.objects.get(user=request.user)
    posts = Post.objects.filter(author=request.user).order_by('-date_posted')
    return render(request, 'users/profile.html',  {'posts': posts, 'profile': profile})

        
def home(request):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post(content=content, author=request.user)
        post.save()

    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'users/home.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if post.author == request.user:
        post.delete()
        messages.success(request, 'Your post has been deleted!')
    else:
        messages.error(request, 'You are not authorized to delete this post.')
    return redirect('profile')

def search(request):
    query = request.GET.get('q')
    results = []
    if query is not None:
        results = Profile.objects.filter(user__username__icontains=query)
    context = {
        'results': results,
        'query': query
    }
    return render(request, 'users/search_results.html', context)

@login_required
def user_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=user_profile.user).order_by('-date_posted')
    context = {
        'user_profile': user_profile,
        'posts': posts
    }
    return render(request, 'users/user_profile.html', context)
    