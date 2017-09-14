from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meta:#元标签
        model = Comment
        fields = ['name','email','url','text']
