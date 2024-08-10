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
        ('email', 'The e-mail must be valid'),
        ('username', 'Max 150 characters, min 4 characters'),
    ])
    def test_fields_helptext(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand([
        ('username', 'Username'),
        ('email', 'E-mail'),
        ('first_name', 'First Name'),
        ('last_name', 'Last Name'),
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
        ('username', 'Write your username'),
        ('first_name', 'Write your first name'),
        ('last_name', 'Write your last name'),
        ('password', 'Password must not be empty'),
        ('password2', 'Please repeat your password'),
        ('email', 'Write your e-mail'),
    ])
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(message, response.content.decode('utf-8'))
        self.assertIn(message, response.context['form'].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'joa'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        message = 'Username must have at least 4 characters'
        self.assertIn(message, response.content.decode('utf-8'))
        self.assertIn(message, response.context['form'].errors.get('username'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'A' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        message = 'Username must have less than 150 characters'
        self.assertIn(message, response.context['form'].errors.get('username'))
        self.assertIn(message, response.content.decode('utf-8'))
