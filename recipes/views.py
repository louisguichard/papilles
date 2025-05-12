from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Recipe
from .forms import RecipeForm


def home(request):
    categories = Category.objects.all()
    return render(request, "recipes/home.html", {"categories": categories})


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    recipes = category.recipes.all()
    return render(
        request,
        "recipes/category.html",
        {
            "category": category,
            "recipes": recipes,
        },
    )


def recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    # Get the first category for the back link (if any)
    first_category = recipe.categories.first()
    return render(
        request,
        "recipes/recipe.html",
        {
            "recipe": recipe,
            "first_category": first_category,
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


def edit_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect("recipe", recipe_slug=recipe.slug)
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request,
        "recipes/create_recipe.html",
        {
            "form": form,
            "edit_mode": True,
            "recipe": recipe,
        },
    )
