from django import forms
from .models import *

class AddPostNews(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField()

class AddPostComment(forms.Form):
    content = forms.CharField()