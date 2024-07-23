from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Seu nome de usuário'),
        ('email', 'Seu email'),
        ('first_name', 'Seu primeiro nome'),
        ('last_name', 'Seu ultimo nome'),
        ('password', 'Sua senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_first_name_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)
