from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser , UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "date_of_birth")  # เพิ่ม profile_image

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['date_of_birth'].required = False  # Make date_of_birth optional

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['bio'].required = False  # Make bio optional
        self.fields['profile_picture'].required = False  # Make profile_picture optional