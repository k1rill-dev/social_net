from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import *

class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Никнейм',max_length=155, widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    password1 = forms.CharField(label='Введите пароль', max_length=155, widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )
    password2 = forms.CharField(label='Подтверждение пароля',max_length=155, widget=forms.PasswordInput(attrs={'class': 'form-control'})
                               )
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', max_length=155, widget=forms.TextInput(attrs={'class': 'form-control'})
                               )
    password = forms.CharField(label='Пароль', max_length=155,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'})
                                )


class UpdateUserForm(forms.ModelForm):
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'exampleInputEmail1'}))

    class Meta:
        model = User
        fields = ['username', 'email']

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_photo', 'date_of_birth']

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        exclude = ['likes', 'author', 'slug']


class CommentForm(forms.ModelForm):
    content = forms.CharField(label='Комментарий', max_length=155, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    class Meta:
        model = Comment
        fields = '__all__'
        exclude = ['likes', 'author', 'publication_date', 'post', 'file']