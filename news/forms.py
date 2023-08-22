from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class AddPostNews(forms.ModelForm):
    class Meta():
        model = News
        fields = ["title", "content"]

class AddPostComment(forms.ModelForm):
    class Meta():
        model = Comment
        fields = ["content"]
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]