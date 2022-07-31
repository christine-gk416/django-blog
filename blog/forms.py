from django import forms
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import Comment, Profile, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body', 'month')


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class PostForm(forms.ModelForm):
   
    class Meta:
        model = Post
        fields = (
            'title', 'status', 'featured_image', 'excerpt', 'content'
            )
        widgets = {
            'excerpt': SummernoteWidget(),
            'content': SummernoteWidget()
        }



class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    name = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio', 'name']
