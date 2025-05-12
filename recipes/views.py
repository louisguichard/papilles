from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Recipe
from .forms import RecipeForm


def home(request):
    categories = Category.objects.all()
    return render(request, "recipes/home.html", {"categories": categories})


def category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    recipes = category.recipes.all()
    return render(
        request,
        "recipes/category.html",
        {
            "category": category,
            "recipes": recipes,
        },
    )


def recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(
        request,
        "recipes/recipe.html",
        {
            "recipe": recipe,
        },
    )


def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = RecipeForm()

    return render(
        request,
        "recipes/create_recipe.html",
        {
            "form": form,
        },
    )
