from django import forms
from core.user.models import User


class ResetPasswordForm(forms.Form):
    id = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    email = forms.CharField(widget=forms.TextInput(attrs={}))

    def clean(self):
        cleaned_data = super(ResetPasswordForm, self).clean()
        email = cleaned_data.get('email')
        users = User.objects.filter(email=email)
        if not users.exists():
            msg = 'El email no esta registrado'
            self.add_error('email', msg)
        else:
            self.cleaned_data['id'] = users[0].id
        return self.cleaned_data


class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={}))
    confirmPassword = forms.CharField(widget=forms.PasswordInput(attrs={}))

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get('password')
        confirmPassword = cleaned_data.get('confirmPassword')
        if password != confirmPassword:
            msg = 'Las contraseñas deben ser iguales'
            self.add_error('password', msg)
