from django import forms 
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=300, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username", "first_name" , "last_name", "email", "password")

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user