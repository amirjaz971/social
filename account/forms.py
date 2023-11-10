from django import forms 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Register_form(forms.Form):
    username=forms.CharField()
    email=forms.EmailField()
    password=forms.CharField(label='password',widget=forms.PasswordInput())
    password_confirm=forms.CharField(label='confirm password',widget=forms.PasswordInput())
    def clean_email(self):
        email=self.cleaned_data['email']
        user=User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('This email already exists!')
        return email
    def clean_username(self):
        username=self.cleaned_data['username']
        user=User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('This username already exists!')
        return username
    def clean(self):
        cd=super().clean()
        p1=cd.get('password')
        p2=cd.get('password_confirm')
        if p1 and p2 and p1!=p2:
            raise ValidationError('Passwords must match!')

class Login_form(forms.Form):
    username=forms.CharField(widget=forms.TextInput())
    password=forms.CharField(widget=forms.PasswordInput())