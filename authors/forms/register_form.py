from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields["username"], "Seu nome de usuário")
        add_placeholder(self.fields["email"], "Seu email")
        add_placeholder(self.fields["first_name"], "Seu primeiro nome")
        add_placeholder(self.fields["last_name"], "Seu ultimo nome")
        add_placeholder(self.fields["password"], "Sua senha")
        add_placeholder(self.fields["password2"], "Confirme sua senha")

    username = forms.CharField(
        label="Username",
        help_text="Max 150 characters, min 4 characters",
        error_messages={
            "required": "Write your username",
            "min_length": "Username must have at least 4 characters",
            "max_length": "Username must have less than 150 characters",
        },
        min_length=4,
        max_length=150,
    )

    first_name = forms.CharField(
        error_messages={"required": "Write your first name"},
        required=True,
        label="First Name",
    )

    last_name = forms.CharField(
        error_messages={"required": "Write your last name"},
        required=True,
        label="Last Name",
    )

    email = forms.EmailField(
        error_messages={"required": "Write your e-mail"},
        required=True,
        label="E-mail",
        help_text="The e-mail must be valid",
    )

    password = forms.CharField(
        required=True,
        error_messages={"required": "Password must not be empty"},
        validators=[strong_password],
        help_text=("Digite uma senha forte!"),
        label="Password",
    )

    password2 = forms.CharField(
        required=True,
        error_messages={"required": "Please repeat your password"},
        help_text=("Digite uma senha forte!"),
        label="Password2",
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]

        labels = {
            "username": "Digite seu usuário",
        }

    def clean_password(self):
        data = self.cleaned_data.get("password")

        return data

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'User e-mail is already in use', code='invalid', )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password != password2:
            password_confirmation_error = ValidationError(
                "Senhas devem ser iguais!", code="invalid"
            )
            raise ValidationError(
                {
                    "password": password_confirmation_error,
                    "password2": [
                        password_confirmation_error,
                    ],
                }
            )
