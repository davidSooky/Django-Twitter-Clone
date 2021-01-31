from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Profile

# Third party imports
from datetime import date, datetime


class RegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text="Enter a valid email address", widget=forms.EmailInput(attrs={"autocomplete":"off"}))
    username = forms.CharField(max_length=40, help_text="Enter a username", widget=forms.TextInput(attrs={"autocomplete":"off"}))
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
        labels = {"dob": "Date of birth"}
        widgets = {
            # Picture fields are formated in such way, that the file picker is not visible, clicking on the pictures opens the file picker
            "cover_pic":forms.FileInput(attrs={"type":"file", "class":"cover-pic", "name":"cover-pic", "id":"cover-pic", "hidden":"true"}),
            "profile_pic":forms.FileInput(attrs={"type":"file", "class":"profile-pic", "name":"profile-pic", "id":"profile-pic", "hidden":"true"}),
            "description":forms.TextInput(attrs={"placeholder":"Say something about yourself..."}),
            "dob":forms.DateInput(attrs={"type":"date"})
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if not field in ["dob", "cover_pic", "profile_pic"]: 
                self.fields[field].widget.attrs["autocomplete"] = "off"

class ProfileRegisterForm(ProfileForm):
    class Meta(ProfileForm.Meta):
        exclude = ["user", "cover_pic", "profile_pic", "description", "country", "email"]
    
    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob is not None:
            dob = datetime.strptime(str(dob), "%Y-%m-%d").date()
            today =  date.today()
            age = today.year - dob.year
            if age < 15:
                raise forms.ValidationError("You have to be at least 15 years old to register.")
        return dob
