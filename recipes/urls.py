from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("category/<slug:category_slug>/", views.category, name="category"),
    path("recipe/<slug:recipe_slug>/", views.recipe, name="recipe"),
    path("create-recipe/", views.create_recipe, name="create_recipe"),
    path("edit-recipe/<slug:recipe_slug>/", views.edit_recipe, name="edit_recipe"),
]
