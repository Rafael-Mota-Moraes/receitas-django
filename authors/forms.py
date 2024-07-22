from django import forms
from django.contrib.auth.models import User


def add_attr(field, attr_name, attr_new_val):
    existing_attr = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing_attr} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    field.widget.attrs['placeholder'] = placeholder_val


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
        })
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Digite novamente sua senha'
        }),
        error_messages={
            'required': 'Senha não pode estar vazia'
        },
        help_text=(
            'Senha deve ter entre 1 e 150 caracteres'
        )
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
