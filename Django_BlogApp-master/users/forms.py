from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'profile_picture']

class CreatePostForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)