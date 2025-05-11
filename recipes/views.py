from django.shortcuts import render, get_object_or_404
from .models import Category


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
