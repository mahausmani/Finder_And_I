from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm, CreatePostForm
from .models import Post
from django.contrib.auth.decorators import login_required

def about(request):
    return render(request, 'users/about.html', {'title':'About'})

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
@login_required
def post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        if content:
            post = Post.objects.create(content=content, author=request.user, image=image)
            return redirect('home')
        
def home(request):
    if request.method == 'POST':
        content = request.POST['content']
        post = Post(content=content, author=request.user)
        post.save()

    posts = Post.objects.all().order_by('-date_posted')
    return render(request, 'users/home.html', {'posts': posts})