from django import forms

class UserCreationForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=255)
    bio = forms.CharField(required=False)

    preferences = forms.CharField(required=False)

class UserValidationForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()
