from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Feedback

User = get_user_model()

# A form that is linked to the User model
class Registration(forms.ModelForm): 
    # Field for entering the password (hidden input box)
    password = forms.CharField(widget=forms.PasswordInput)
    
    # Second password field to confirm the first one
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        # This form uses the built-in User model
        model = User
        
        # These are the User model fields that will appear on the form
        fields = ['username', 'email', 'password']
    
    def clean_email(self):
        """Reject registration if the email is already used (case-insensitive)."""
        email = (self.cleaned_data.get('email') or '').strip()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


    # This method checks the entire form after all fields are entered
    def clean(self):
        # First let Django clean the data normally
        cleaned_data = super().clean()

        # Get the password the user typed
        password = cleaned_data.get('password')
        
        # Get the confirm password value
        confirm = cleaned_data.get('confirm_password')

        # If the two passwords are different, stop the form with an error
        if password != confirm:
            raise forms.ValidationError("Passwords do not match")
        
        # Return all cleaned values back
        return cleaned_data


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name','email','message']

 