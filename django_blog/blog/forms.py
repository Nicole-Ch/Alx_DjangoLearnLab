from .models import Post
from django import forms

class BlogForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']