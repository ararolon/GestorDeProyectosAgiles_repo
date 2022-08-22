from allauth.socialaccount.models import SocialApp
from django import forms

class SocialAppForm(forms.ModelForm):
    class Meta:
        model = SocialApp
        fields = ['client_id','secret','provider']