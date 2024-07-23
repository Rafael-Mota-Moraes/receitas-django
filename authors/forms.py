from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            ('Senha deve ter pelo menos uma letra maiúscula'
             'uma letra minúscula'
             'e um número'
             'Tamanho da senha tem que ser de no mínimo 8 caracteres'),
            code='invalid')


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'],
                        'Seu nome de usuário')
        add_placeholder(self.fields['email'], 'Seu email')
        add_placeholder(self.fields['first_name'], 'Seu primeiro nome')
        add_placeholder(self.fields['last_name'], 'Seu ultimo nome')

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite sua senha'
        }),
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite novamente sua senha'
        }),
        error_messages={
            'required': 'Senha não é forte o suficiente'
        },
        help_text=(
            'Senha deve ter pelo menos uma letra maiúscula'
            'uma letra minúscula'
            'e um número'
            'Tamanho da senha tem que ser de no mínimo 8 caracteres'
        ),

    )

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
            'username': 'Digite seu usuário',
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

    def clean_password(self):
        data = self.cleaned_data.get('password')

        if 'atenção' in data:
            raise ValidationError(
                'Valor inválido atenção',
                code='invalid',
                params={'value': 'atenção'}
            )

        return data

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Senhas devem ser iguais!',
                code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })
