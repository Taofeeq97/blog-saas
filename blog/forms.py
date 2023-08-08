from django import forms
from django.contrib.auth.models import User
# from .models import Tenant

class TenantCreationForm(forms.Form):
    first_name = forms.CharField(label="First Name", required=True)
    last_name = forms.CharField(label="Last Name", required=True)
    username = forms.CharField(label="Username", required=True)
    blog_name = forms.CharField(label="Blog Name", required=True)
    domain_name = forms.CharField(label="Preferred Name (Subdomain)", required=True)
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True)
    
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        

class UserCreateForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(), required=True)

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(label="Password", widget=forms.PasswordInput(), required=True)


