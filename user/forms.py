from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Enter a valid email address", widget=forms.EmailInput(attrs={"autocomplete":"off"}))
    username = forms.CharField(max_length=40, help_text="Enter a username", widget=forms.TextInput(attrs={"autocomplete":"off"}))
    # dob = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError("This email address is already in use. Please select a different email address.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"autocomplete":"off", "id":"user"}))
    password = forms.CharField(widget=forms.PasswordInput())



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ["user"]
        widgets = {
            "cover_pic":forms.FileInput(attrs={"type":"file", "class":"cover-pic", "name":"cover-pic", "id":"cover-pic", "hidden":"true"}),
            "profile_pic":forms.FileInput(attrs={"type":"file", "class":"profile-pic", "name":"profile-pic", "id":"profile-pic", "hidden":"true"}),
            "email":forms.EmailInput(attrs={"autocomplete":"off"})
        }
    
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].attrs.autocomplete = "off"