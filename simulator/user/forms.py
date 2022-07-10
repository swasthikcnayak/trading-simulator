from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import Profile


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name','last_name','image']
        labels = {
            'image': 'Profile picture'
        }
