from django import forms
from .models import Comment
from .models import Post, Category, Location
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# ДОБАВЬТЕ ЭТУ ФОРМУ ДЛЯ СОЗДАНИЯ ПОСТОВ:
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category', 'location']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 10}),
        }
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Оставьте ваш комментарий...'
            }),
        }