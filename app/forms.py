from django import forms
from django.db import models


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )


class SignUpForm(forms.Form):
    username = forms.CharField(
        label='Usuario',
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        })
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'minlength': 5,
            'maxlength': 20,
            'required pattern': '^[A-za-z0-9]+$',
            'title': 'La contraseña debe tener entre 5 y 20 caracteres de' +
                ' longitud. Únicamente debe contener letras y números.'
        })
    )
    confirm_password = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'minlength': 5,
            'maxlength': 20,
            'required pattern': '^[A-za-z0-9]+$',
            'title': 'Vuelva a escribir su contraseña.'
        })
    )
