from django import forms


from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Contact
from django.forms import ModelForm

class SignupForm(UserCreationForm):
    first_name=forms.CharField(max_length=120)
    last_name=forms.CharField(max_length=120)
    email=forms.EmailField(max_length=200)
    
    class Meta:
        model=User
        fields=('username','first_name','last_name','email','password1','password2',)
        
class ContactForm(ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'First Name'}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    phone=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'91+ '}))
    description=forms.CharField(widget=forms.Textarea(attrs={'placeholder':'Write your query'}))
    class Meta:
        model=Contact
        fields="__all__"