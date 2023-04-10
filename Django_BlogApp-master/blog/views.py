# from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .forms import BlogEntryForm
# from .models import BlogEntry
# from django.contrib import messages
# from django.shortcuts import get_object_or_404, redirect
# from django.shortcuts import render, get_object_or_404
# from .models import BlogEntry
# from django.contrib import messages
# from .models import BlogEntry


# @login_required
# def create_blog_entry(request):
#     if request.method == 'POST':
#         form = BlogEntryForm(request.POST)
#         if form.is_valid():
#             blog_entry = form.save(commit=False)
#             blog_entry.author = request.user
#             blog_entry.save()
#             messages.success(request, 'Your blog entry has been created!')
#             return redirect('blog-home')
#     else:
#         form = BlogEntryForm()
#     return render(request, 'blog/create_blog_entry.html', {'form': form})

@login_required
def home(request):
    context = {
        'user': request.user,
    }
    return render(request, 'blog/home.html', context)
# def home(request):
#     context = {
#         'posts': BlogEntry.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


# @login_required
# def delete_blog_entry(request, post_id):
#     post = get_object_or_404(BlogEntry, id=post_id)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, 'Your blog entry has been deleted.')
#         return redirect('blog-home')
#     return render(request, 'blog/delete_blog_entry.html', {'post': post})
# @login_required
# def delete_blog_entry(request, post_id):
#     post = get_object_or_404(BlogEntry, id=post_id)
#     print(post.author)
#     print(request.user)
#     if request.method == 'POST':
#         post.delete()
#         messages.success(request, 'Your blog entry has been deleted.')
#         return redirect('blog-home')
#     return render(request, 'blog/delete_blog_entry.html', {'post': post})

# def blog_detail(request, pk):
#     post = get_object_or_404(BlogEntry, pk=pk)
#     return render(request, 'blog/post.html', {'post': post})

# def blog_post(request, post_id):
#     post = get_object_or_404(BlogEntry, id=post_id)
#     return render(request, 'blog/post.html', {'post': post})




def about(request):
    return render(request, 'blog/about.html', {'title':'About'})



# @login_required
# def create_blog_entry(request):
#     if request.method == 'POST':
#         form = BlogEntryForm(request.POST)
#         if form.is_valid():
#             blog_entry = form.save(commit=False)
#             blog_entry.author = request.user
#             blog_entry.save()
#             return redirect('blog-home')
#     else:
#         form = BlogEntryForm()
#     return render(request, 'blog/create_blog_entry.html', {'form': form})


