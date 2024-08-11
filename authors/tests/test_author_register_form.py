from django.test import TestCase as DjangoTestCase
from unittest import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand(
        [
            ("username", "Seu nome de usuário"),
            ("email", "Seu email"),
            ("first_name", "Seu primeiro nome"),
            ("last_name", "Seu ultimo nome"),
            ("password", "Sua senha"),
            ("password2", "Confirme sua senha"),
        ]
    )
    def test_fields_placeholder(self, field, placeholder):
        form = RegisterForm()
        current_placeholder = form[field].field.widget.attrs["placeholder"]
        self.assertEqual(current_placeholder, placeholder)

    @parameterized.expand(
        [
            ("password", "Digite uma senha forte!"),
            ("email", "The e-mail must be valid"),
            ("username", "Max 150 characters, min 4 characters"),
        ]
    )
    def test_fields_helptext(self, field, needed):
        form = RegisterForm()
        current = form[field].field.help_text
        self.assertEqual(current, needed)

    @parameterized.expand(
        [
            ("username", "Username"),
            ("email", "E-mail"),
            ("first_name", "First Name"),
            ("last_name", "Last Name"),
            ("password", "Password"),
            ("password2", "Password2"),
        ]
    )
    def test_fields_label(self, field, needed):
        form = RegisterForm()
        current = form[field].field.label
        self.assertEqual(current, needed)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs) -> None:
        self.form_data = {
            "username": "user",
            "first_name": "fisrt",
            "last_name": "last",
            "email": "email@email.com",
            "password": "Str0ngP@ssw0rd1",
            "password2": "Str0ngP@ssw0rd1",
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand(
        [
            ("username", "Write your username"),
            ("first_name", "Write your first name"),
            ("last_name", "Write your last name"),
            ("password", "Password must not be empty"),
            ("password2", "Please repeat your password"),
            ("email", "Write your e-mail"),
        ]
    )
    def test_fields_cannot_be_empty(self, field, message):
        self.form_data[field] = ""
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(message, response.content.decode("utf-8"))
        self.assertIn(message, response.context["form"].errors.get(field))

    def test_username_field_min_length_should_be_4(self):
        self.form_data["username"] = "joa"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        message = "Username must have at least 4 characters"
        self.assertIn(message, response.content.decode("utf-8"))
        self.assertIn(message, response.context["form"].errors.get("username"))

    def test_username_field_max_length_should_be_150(self):
        self.form_data["username"] = "A" * 151
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)
        message = "Username must have less than 150 characters"
        self.assertIn(message, response.context["form"].errors.get("username"))
        self.assertIn(message, response.content.decode("utf-8"))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data["password"] = "abc123"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)

        message = (
            "Senha deve ter pelo menos uma letra maiúscula"
            "uma letra minúscula"
            "e um número"
            "Tamanho da senha tem que ser de no mínimo 8 caracteres"
        )

        self.assertIn(message, response.context["form"].errors.get("password"))
        self.assertIn(message, response.content.decode("utf-8"))

        self.form_data["password"] = "@A123abc123"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(
            message, response.context["form"].errors.get("password"))
        self.assertNotIn(message, response.content.decode("utf-8"))

    def test_password_and_password_confirmation_are_equal(self):
        self.form_data["password"] = "@A123abc123"
        self.form_data["password2"] = "@A123abc1234"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'Senhas devem ser iguais!'

        self.assertIn(message, response.context["form"].errors.get("password"))
        self.assertIn(message, response.content.decode("utf-8"))

        self.form_data["password"] = "@A123abc123"
        self.form_data["password2"] = "@A123abc123"
        url = reverse("authors:register_create")
        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'Senhas devem ser iguais!'

        self.assertNotIn(message, response.content.decode("utf-8"))

    def test_send_get_request_to_registration_create_view_returns_404(self):
        url = reverse("authors:register_create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_email_field_must_be_unique(self):
        url = reverse("authors:register_create")

        self.client.post(url, data=self.form_data, follow=True)

        response = self.client.post(url, data=self.form_data, follow=True)

        message = 'User e-mail is already in use'
        self.assertIn(message,
                      response.context["form"].errors.get("email"))
        self.assertIn(message, response.content.decode("utf-8"))

    def test_author_created_can_login(self):
        url = reverse("authors:register_create")

        self.form_data.update({
            'username': 'testuser',
            'password': '@Bc123456',
            'password2': '@Bc123456'
        })
        self.client.post(url, data=self.form_data, follow=True)
        is_authenticated = self.client.login(
            username='testuser',
            password='@Bc123456'
        )

        self.assertTrue(is_authenticated)
