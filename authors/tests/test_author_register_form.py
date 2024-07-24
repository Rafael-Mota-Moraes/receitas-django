from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('username', 'Seu nome de usuário'),
        ('email', 'Seu email'),
        ('first_name', 'Seu primeiro nome'),
        ('last_name', 'Seu ultimo nome'),
        ('password', 'Sua senha'),
        ('password2', 'Confirme sua senha'),
    ])
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs['placeholder']
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand([
        ('password',
            'Digite uma senha forte!'),
        ('email', 'Digite um email'),
    ])
    def test_fields_helptext(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Digite seu usuário'),
        ('email', 'Endereço de email'),
        ('first_name', 'Primeiro nome'),
        ('last_name', 'Último nome'),
        ('password', 'Password'),
        ('password2', 'Password2'),
    ])
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            'username': 'user',
            'first_name': 'fisrt',
            'last_name': 'last',
            'email': 'email@email.com',
            'password': 'Str0ngP@ssw0rd1',
            'password2': 'Str0ngP@ssw0rd1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('username', 'Campo é obrigatório')
    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(message, response.content.decode('utf-8'))
