from .models import Post, Comment
from django import forms


class BlogForm(forms.ModelForm):
    tags = TagField(required=False, widget=TagWidget())

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3}),
        }