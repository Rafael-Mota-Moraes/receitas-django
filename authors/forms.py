from django import forms
from django.contrib.auth.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]

        labels = {
            'username': 'Digite seu usuário'
        }

        help_texts = {
            'email': 'Digite um email'
        }

        error_messages = {
            'username': {
                'required': 'Campo é obrigatório'
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Digite seu nome'}),
        }
