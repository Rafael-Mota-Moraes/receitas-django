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
        add_placeholder(self.fields['password'], 'Sua senha')
        add_placeholder(self.fields['password2'], 'Confirme sua senha')

    username = forms.CharField(
        label='Username',
        help_text='Max 150 characters, min 4 characters',
        error_messages={'required': 'Write your username',
                        'min_length': 'Username must have at least 4 characters',
                        'max_length': 'Username must have less than 150 characters',
                        },
        min_length=4, max_length=150
    )

    first_name = forms.CharField(
        error_messages={'required': 'Write your first name'},
        required=True,
        label='First Name'
    )

    last_name = forms.CharField(
        error_messages={'required': 'Write your last name'},
        required=True,
        label='Last Name'
    )

    email = forms.EmailField(
        error_messages={'required': 'Write your e-mail'},
        required=True,
        label='E-mail',
        help_text='The e-mail must be valid'
    )

    password = forms.CharField(
        required=True,
        error_messages={'required': 'Password must not be empty'},
        validators=[strong_password],
        help_text=(
            'Digite uma senha forte!'
        ),
        label='Password',
    )

    password2 = forms.CharField(
        required=True,
        error_messages={
            'required': 'Please repeat your password'
        },
        help_text=(
            'Digite uma senha forte!'
        ),
        label='Password2',
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
