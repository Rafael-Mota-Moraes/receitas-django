from django.urls import reverse, resolve
from recipes import views
from recipes.tests.test_recipe_base import RecipeTestBase
from unittest import skip


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse("recipes:category",
                       kwargs={"category_id": 10000}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(
            reverse("recipes:category", kwargs={"category_id": 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):
        needed_title = "Category test"
        self.make_recipe(title=needed_title)
        response = self.client.get(reverse("recipes:category", args=(1,)))
        content = response.content.decode("utf-8")

        self.assertIn(needed_title, content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        """Test recipe is published False dont show"""
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse("recipes:category", args=(recipe.category.id,))
        )

        self.assertEqual(response.status_code, 404)
