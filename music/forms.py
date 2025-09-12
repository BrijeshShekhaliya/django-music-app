from django import forms
from allauth.account.forms import SignupForm
from .models import Song, CustomUser

class CustomSignupForm(SignupForm):
    mobile_number = forms.CharField(max_length=15, label='Mobile Number', required=True)
    age = forms.IntegerField(label='Age', required=True)

    def save(self, request):
        user = super().save(request)  # allauth saves the user

        # Validate mobile number
        mobile_number = self.cleaned_data['mobile_number'].strip()
        if not mobile_number:
            raise forms.ValidationError("Mobile number cannot be empty.")
        if CustomUser.objects.filter(mobile_number=mobile_number).exclude(pk=user.pk).exists():
            raise forms.ValidationError("This mobile number is already registered.")

        # Assign custom fields
        user.mobile_number = mobile_number
        user.age = self.cleaned_data['age']
        user.save()  # save again with custom fields

        return user
    
class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['name', 'theme_image', 'author_name', 'song_file']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_avatar']