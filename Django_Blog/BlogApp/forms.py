from django import forms
from .models import article

class createForm(forms.ModelForm):
    class Meta:
        model=article
        fields=[
            'title',
            'body',
            'image',
            'category',
        ]