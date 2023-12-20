from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def setUp(self) -> None:
        category = Category.objects.create(name='')
        author = User.objects.create_user(
            first_name='user',
            last_name='name',
            username='username',
            password='123456',
            email='user@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='recipe title',
            description='recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='minutos',
            servings=5,
            servings_unit='porções',
            preparation_steps='recipe preparation steps',
            preparation_steps_is_html=False,
            is_published=True,
        )

        return super().setUp()
