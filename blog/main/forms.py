from .models import *
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class LoginUserForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(    attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']
        widgets = {
            'username':     forms.TextInput(    attrs={'class': 'form-control'}),
            'password1':    forms.PasswordInput(attrs={'class': 'form-control'}),
            'password1':    forms.PasswordInput(attrs={'class': 'form-control'}),
            'email':        forms.EmailInput(   attrs={'class': 'form-control'}),
        }

class AddPostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), label='Тэги')
    class Meta:
        model = Post
        fields = ['title', 'description', 'content', 'is_published', 'tags']
        widgets = {
            'title':        forms.TextInput(attrs={'class': 'form-control'}),
            'description':  forms.Textarea( attrs={'class': 'form-control', 'rows': '4'}),
            'content':      forms.Textarea( attrs={'class': 'form-control', 'rows': '10'}),
            'tags':         forms.CheckboxSelectMultiple(attrs={'class': 'column-checkbox'})
        }

class AddCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': '3'})
        }

class SearchForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'search-form',
                'placeholder': 'введите название статьи'})
        }

