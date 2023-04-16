from django import forms
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

class CreatePostForm(ModelForm):
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        fields = ['content', 'image']
        widgets = {'content': forms.Textarea()}