# music/forms.py
from django import forms
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from .models import Song, CustomUser

class CustomSignupForm(SignupForm):
    mobile_number = forms.CharField(max_length=15, label='Mobile Number', required=True)
    age = forms.IntegerField(label='Age', required=True)
    role = forms.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number', '').strip()
        if not mobile:
            raise ValidationError("Mobile number cannot be empty.")
        if CustomUser.objects.filter(mobile_number=mobile).exists():
            raise ValidationError("This mobile number is already registered.")
        return mobile

    def save(self, request):
        user = super().save(request)

        user.mobile_number = self.cleaned_data["mobile_number"].strip()
        user.age = self.cleaned_data["age"]
        user.role = self.cleaned_data["role"]
        user.save()
        return user

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'theme_image', 'author_name', 'song_file']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_avatar']
