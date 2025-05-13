from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("collection/<slug:collection_slug>/", views.collection, name="collection"),
    path("recipe/<slug:recipe_slug>/", views.recipe, name="recipe"),
    path("create-recipe/", views.create_recipe, name="create_recipe"),
    path("edit-recipe/<slug:recipe_slug>/", views.edit_recipe, name="edit_recipe"),
]
