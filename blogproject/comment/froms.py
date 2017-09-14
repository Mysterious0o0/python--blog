from django import forms
from .models import Comment
class CommentForm(forms.ModelForm):
    class Meat:
        model = Comment
        fieds = ['name','email','url','text']
