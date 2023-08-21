from django import forms
from .models import *

class AddPostNews(forms.ModelForm):
    class Meta():
        model = News
        fields = ["title", "content"]

class AddPostComment(forms.Form):
    content = forms.CharField()