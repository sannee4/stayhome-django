from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Post, Category, Tag, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['article_image', 'title', 'content', 'category', 'tags']
        exclude = ['author']

    article_image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'profile-form__file-input form-panel__body-item', 'id': 'profile-form__file-input'}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-panel__body-item', 'placeholder': 'Заголовок'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'input form-panel__body-item', 'placeholder': 'Текст'}))
    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(), widget=forms.SelectMultiple(attrs={'class': 'select-multiple'}))
    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(attrs={'class': 'select'}))


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'input form-panel__body-item', 'placeholder': 'Название тега'}))


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['author', 'post']

    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'input form-panel__body-item', 'placeholder': 'Комментарий'}))
