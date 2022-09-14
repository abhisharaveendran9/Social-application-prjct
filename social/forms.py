from django import forms
from django.contrib.auth.models import User

# class RegistrationForm(forms.Form):
#     first_name=forms.CharField()
#     last_name=forms.CharField()
#     email=forms.EmailField()
#     username=forms.CharField()
#     password=forms.CharField()

class RegistrationForm(forms.ModelForm):
    class Meta:
        model=User
        fields=[
            "first_name","last_name","email","username","email","password"
        ]


class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()