from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from authors.forms.recipe_form import AuthorRecipeForm
from recipes.models import Recipe


@method_decorator(
    login_required(login_url='authors:login', redirect_field_name='next'),
    name='dispatch'
)
class DashboardRecipe(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_recipe(self, id=None):
        recipe = None

        if id is not None:
            recipe = Recipe.objects.get(
                is_published=False,
                author=self.request.user,
                pk=id,
            )

            if not recipe:
                raise Http404()

            return recipe

    def render_recipe(self, form):
        return render(self.request, 'authors/pages/dashboard_recipe.html', {
            "form": form,
        })

    def get(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(instance=recipe)

        return self.render_recipe(form)

    def post(self, request, id=None):
        recipe = self.get_recipe(id)

        form = AuthorRecipeForm(
            data=request.POST or None,
            files=request.FILES or None,
            instance=recipe
        )

        if form.is_valid():
            # Agora o form é valido e eu posso tentar salvar
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False

            recipe.save()
            messages.success(request, "Sua receita foi salva com sucesso!")

            return redirect(reverse("authors:dashboard_recipe_edit", args=(
                recipe.id,
            )))

        return self.render_recipe(form)
