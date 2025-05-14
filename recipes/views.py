from django.shortcuts import render, get_object_or_404, redirect
from .models import Collection, Recipe, Gallery
from .forms import RecipeForm, CollectionForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


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


def collection(request, username, collection_slug):
    collection = get_object_or_404(
        Collection, user__username=username, slug=collection_slug
    )
    recipes = collection.recipes.all()
    return render(
        request,
        "recipes/collection.html",
        {
            "collection": collection,
            "recipes": recipes,
        },
    )


def recipe(request, username, recipe_slug):
    recipe = get_object_or_404(Recipe, user__username=username, slug=recipe_slug)
    # Get the first collection for the back link (if any)
    first_collection = recipe.collections.first()

    # Get user collections for the add to collection form
    user_collections = []
    if request.user.is_authenticated and request.user != recipe.user:
        user_collections = Collection.objects.filter(user=request.user)

    return render(
        request,
        "recipes/recipe.html",
        {
            "recipe": recipe,
            "first_collection": first_collection,
            "is_owner": request.user == recipe.user,
            "user": request.user,
            "user_collections": user_collections,
        },
    )


@login_required
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(user=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            form.save_m2m()  # Save many-to-many fields
            return redirect(
                "recipe", username=request.user.username, recipe_slug=recipe.slug
            )
    else:
        form = RecipeForm(user=request.user)

    return render(
        request,
        "recipes/create_recipe.html",
        {
            "form": form,
            "edit_mode": False,
        },
    )


@login_required
def edit_recipe(request, recipe_slug):
    recipe = get_object_or_404(Recipe, slug=recipe_slug, user=request.user)

    # Check if the user is the owner of the recipe
    if request.user != recipe.user:
        return HttpResponseForbidden("You don't have permission to edit this recipe")

    if request.method == "POST":
        form = RecipeForm(
            user=request.user, data=request.POST, files=request.FILES, instance=recipe
        )
        if form.is_valid():
            form.save()
            return redirect(
                "recipe", username=request.user.username, recipe_slug=recipe.slug
            )
    else:
        form = RecipeForm(user=request.user, instance=recipe)

    return render(
        request,
        "recipes/create_recipe.html",
        {
            "form": form,
            "edit_mode": True,
            "recipe": recipe,
        },
    )


@login_required
def create_collection(request):
    if request.method == "POST":
        form = CollectionForm(request.POST, request.FILES)
        if form.is_valid():
            collection = form.save(commit=False)
            collection.user = request.user
            collection.save()
            return redirect("profile")
    else:
        form = CollectionForm()

    return render(
        request,
        "recipes/create_collection.html",
        {
            "form": form,
            "edit_mode": False,
        },
    )


@login_required
def edit_collection(request, collection_slug):
    collection = get_object_or_404(Collection, slug=collection_slug, user=request.user)

    # Check if user is allowed to edit this collection
    if collection.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden(
            "You don't have permission to edit this collection"
        )

    if request.method == "POST":
        form = CollectionForm(request.POST, request.FILES, instance=collection)
        if form.is_valid():
            form.save()
            return redirect(
                "collection",
                username=request.user.username,
                collection_slug=collection.slug,
            )
    else:
        form = CollectionForm(instance=collection)

    return render(
        request,
        "recipes/create_collection.html",
        {
            "form": form,
            "collection": collection,
            "edit_mode": True,
        },
    )


@login_required
def delete_collection(request, collection_slug):
    collection = get_object_or_404(Collection, slug=collection_slug, user=request.user)

    # Check if user is allowed to delete this collection
    if collection.user != request.user and not request.user.is_staff:
        return HttpResponseForbidden(
            "You don't have permission to delete this collection"
        )

    if request.method == "POST":
        collection.delete()
        return redirect("profile")

    return render(
        request,
        "recipes/delete_collection.html",
        {
            "collection": collection,
        },
    )


@login_required
def add_to_collection(request, username, recipe_slug):
    # Get the original recipe
    original_recipe = get_object_or_404(
        Recipe, user__username=username, slug=recipe_slug
    )

    # Check if the user is trying to add their own recipe
    if request.user == original_recipe.user:
        messages.error(
            request,
            "Vous ne pouvez pas ajouter votre propre recette à vos collections.",
        )
        return redirect("recipe", username=username, recipe_slug=recipe_slug)

    if request.method == "POST":
        # Get selected collections from the form
        collection_ids = request.POST.getlist("collections[]")

        if not collection_ids:
            messages.error(request, "Veuillez sélectionner au moins une collection.")
            return redirect("recipe", username=username, recipe_slug=recipe_slug)

        added_collections = []
        for collection_id in collection_ids:
            try:
                collection = Collection.objects.get(id=collection_id, user=request.user)
                # Check if this recipe is already in the collection
                if not collection.recipes.filter(id=original_recipe.id).exists():
                    # Add the original recipe to the user's collection
                    collection.recipes.add(original_recipe)
                    added_collections.append(collection.name)
            except Collection.DoesNotExist:
                continue

        if added_collections:
            collection_names = ", ".join(added_collections)
            messages.success(
                request,
                f"Recette ajoutée aux collections suivantes : {collection_names}",
            )
        else:
            messages.info(request, "Aucune collection valide n'a été sélectionnée.")

        return redirect("recipe", username=username, recipe_slug=recipe_slug)

    # If GET request, redirect back to recipe
    return redirect("recipe", username=username, recipe_slug=recipe_slug)
