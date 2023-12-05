from django import forms
from django.contrib.auth.password_validation import validate_password
from .models import Account

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phonenumber', 'username', 'email', 'password']
        widgets = {'password': forms.PasswordInput()}

    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except forms.ValidationError as error:
            self.add_error('password', error)
        return password

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
