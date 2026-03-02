from django import forms
from django.contrib.auth import get_user_model #ensures that even if you change your User model name later, this form won't break

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput) #(******)

    class Meta:
        model = User
        fields = ["email", "username", "password"] #form exactly which fields to show the usee

    def save(self, commit=True):
        user = super().save(commit=False) #creates the user object in the computer's memory but pauses before sending it to the database
        user.set_password(self.cleaned_data["password"]) #When a user submits a form, Django runs validation (checking if the email is valid, etc.). Once the data passes these checks, it is stored in a dictionary called cleaned_data
        if commit:
            user.save()
        return user