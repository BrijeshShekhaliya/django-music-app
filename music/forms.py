# music/forms.py
from django import forms
from allauth.account.forms import SignupForm
from django.core.exceptions import ValidationError
from .models import Song, CustomUser

class CustomSignupForm(SignupForm):
    mobile_number = forms.CharField(max_length=15, label='Mobile Number', required=True)
    age = forms.IntegerField(label='Age', required=True)

    def clean_mobile_number(self):
        mobile = self.cleaned_data.get('mobile_number', '').strip()
        if not mobile:
            raise ValidationError("Mobile number cannot be empty.")
        # Optionally normalize here (remove spaces, dashes, leading +, etc.)
        if CustomUser.objects.filter(mobile_number=mobile).exists():
            raise ValidationError("This mobile number is already registered.")
        return mobile

    def save(self, request):
        # Let allauth create the base user
        user = super().save(request)

        mobile = self.cleaned_data.get('mobile_number', '').strip()
        age = self.cleaned_data.get('age')

        # final check to avoid race condition
        if CustomUser.objects.filter(mobile_number=mobile).exclude(pk=user.pk).exists():
            raise ValidationError("This mobile number is already registered.")

        user.mobile_number = mobile
        user.age = age
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
