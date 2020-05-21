from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import UserProfile


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Твой никнейм'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'Твоя Эл. почта'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Твой пароль'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Твой пароль еще раз'}))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'Твой никнейм'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'Твой пароль'}))


class EditProfileForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'profile-form__file-input profile-form__file-input_profile', 'id': 'profile-form__file-input'}))


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']
        exclude = ['user']

    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'profile-form__file-input', 'id': 'profile-form__file-input'}))
