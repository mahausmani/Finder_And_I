from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm, CreatePostForm
from .models import Post, Profile, FriendRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404, redirect

def send_friend_request(request, username):
    to_user = get_object_or_404(User, username=username)
    friend_request = FriendRequest(from_user=request.user, to_user=to_user)
    friend_request.save()
    return redirect('user_profile', username=username)

def accept_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user != request.user:
        return redirect('home')
    friend_request.from_user.profile.friends.add(friend_request.to_user)
    friend_request.to_user.profile.friends.add(friend_request.from_user)
    friend_request.delete()
    return redirect('home')

def reject_friend_request(request, request_id):
    friend_request = get_object_or_404(FriendRequest, id=request_id)
    if friend_request.to_user != request.user:
        return redirect('home')
    friend_request.delete()
    return redirect('home')

# @login_required
# def unfriend(request, username):
#     friend = User.objects.get(username=username)
#     profile = Profile.objects.get(user=request.user)
#     profile.friends.remove(friend)
#     return redirect('your_friends')

# @login_required
# def unfriend(request, username):
#     friend = User.objects.get(username=username)
#     profile = User.objects.get(username=request.user.username)
#     user_profile = Profile.objects.get(user=profile)
#     friend_profile = Profile.objects.get(user=friend)
#     user_profile.friends.remove(friend)
#     friend_profile.friends.remove(profile)
#     return redirect('your_friends')

@login_required
def unfriend(request, username):
    friend = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=request.user)
    friend_profile = Profile.objects.get(user=friend)
    profile.friends.remove(friend)
    friend_profile.friends.remove(request.user)
    return redirect('your_friends')

@login_required
def your_friends(request):
    profile = Profile.objects.get(user=request.user)
    friends = profile.friends.all()
    return render(request, 'users/your_friends.html', {'friends': friends})
    

@login_required
def friend_requests(request):
    friend_requests = FriendRequest.objects.filter(to_user=request.user)
    return render(request, 'users/friend_requests.html', {'friend_requests': friend_requests})

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = Profile.objects.get_or_create(user=instance)


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

# @login_required
# def user_profile(request, username):
#     user_profile = get_object_or_404(Profile, user__username=username)
#     posts = Post.objects.filter(author=user_profile.user).order_by('-date_posted')
#     context = {
#         'user_profile': user_profile,
#         'posts': posts,
#     }
#     return render(request, 'users/user_profile.html', context)

@login_required
def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.get(user=user)
    friend_request_sent = FriendRequest.objects.filter(from_user=request.user, to_user=user).exists()
    posts = Post.objects.filter(author=user)

    context = {
        'user_profile': user_profile,
        'posts': posts,
        'friend_request_sent': friend_request_sent
    }
    return render(request, 'users/user_profile.html', context)

    