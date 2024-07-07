from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_has_raises_error_if__title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # validação ocorre aqui!
