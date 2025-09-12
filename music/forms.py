# music/forms.py (Updated)

from django import forms
# Import the base SignupForm from allauth
from allauth.account.forms import SignupForm
from .models import Song, CustomUser

# --- Your other forms are unchanged ---
class SongForm(forms.ModelForm):
    # ...
    pass

class UserUpdateForm(forms.ModelForm):
    class Meta:  # This block is crucial
        model = CustomUser
        fields = ['first_name', 'last_name', 'profile_avatar']


# === REPLACE YOUR OLD CustomSignupForm WITH THIS ===
class CustomSignupForm(SignupForm): # Inherit from allauth's SignupForm
    mobile_number = forms.CharField(max_length=15, label='Mobile Number', required=True)
    age = forms.IntegerField(label='Age', required=True)

    def save(self, request):
        # Call the parent class's save method to create the user
        user = super(CustomSignupForm, self).save(request)
        
        # Add our custom data to the user object
        user.mobile_number = self.cleaned_data['mobile_number']
        user.age = self.cleaned_data['age']
        
        # Save the user object again with the new data
        user.save()
        
        return user