from django.shortcuts import render, get_object_or_404, redirect
from .models import Collection, Recipe, Gallery
from .forms import RecipeForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def home(request):
    if not request.user.is_authenticated:
        return redirect("galleries")

    return redirect("my_collections")


def galleries(request):
    galleries = Gallery.objects.all()
    return render(request, "recipes/galleries.html", {"galleries": galleries})


def gallery(request, gallery_slug):
    gallery = get_object_or_404(Gallery, slug=gallery_slug)
    recipes = gallery.recipes.all()
    return render(
        request,
        "recipes/gallery.html",
        {
            "gallery": gallery,
            "recipes": recipes,
        },
    )


@login_required
def my_collections(request):
    collections = Collection.objects.filter(user=request.user)
    return render(request, "recipes/my_collections.html", {"collections": collections})


def collection(request, collection_slug):
    collection = get_object_or_404(Collection, slug=collection_slug)
    recipes = collection.recipes.all()
    return render(
        request,
        "recipes/collection.html",
        {
            "collection": collection,
            "recipes": recipes,
        },
    )


def recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)
    # Get the first collection for the back link (if any)
    first_collection = recipe.collections.first()
    return render(
        request,
        "recipes/recipe.html",
        {
            "recipe": recipe,
            "first_collection": first_collection,
            "is_owner": request.user == recipe.user,
        },
    )


@login_required
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()  # Save many-to-many fields
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


@login_required
def edit_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug)

    # Check if the user is the owner of the recipe
    if request.user != recipe.user:
        return HttpResponseForbidden("You don't have permission to edit this recipe")

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
