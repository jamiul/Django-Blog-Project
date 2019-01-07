from django import forms
from .models import article, author, Comment, category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class createForm(forms.ModelForm):
    class Meta:
        model=article
        fields=[
            'title',
            'body',
            'image',
            'category',
        ]

class registrationForm(UserCreationForm):
   class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'password1',
            'password2',
        ] 
class authorForm(forms.ModelForm):
    class Meta:
        model=author
        fields=[
            'profile_picture',
            'details',
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=[
            'name',
            'email',
            'post_comment',
        ]  

class createTopicsForm(forms.ModelForm):
    class Meta:
        model=category
        fields=[
            'name',
        ]                                          