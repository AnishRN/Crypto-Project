from django import forms

class CustomSignUpForm(forms.Form):
    User_name = forms.CharField(max_length=100)
    Phone_number = forms.CharField(max_length=100)
    Email = forms.EmailField()
    Password = forms.CharField(widget=forms.PasswordInput)
