from django import forms 
from users.models import CustomUser

class RegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=300, widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ("username", "first_name" , "last_name", "email", "password", 'photo')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "first_name" , "last_name", "email", 'photo')