from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("galleries/", views.galleries, name="galleries"),
    path("gallery/<slug:gallery_slug>/", views.gallery, name="gallery"),
    path("my-collections/", views.my_collections, name="my_collections"),
    path(
        "collection/<str:username>/<slug:collection_slug>/",
        views.collection,
        name="collection",
    ),
    path("recipe/<str:username>/<slug:recipe_slug>/", views.recipe, name="recipe"),
    path("create-recipe/", views.create_recipe, name="create_recipe"),
    path("edit-recipe/<slug:recipe_slug>/", views.edit_recipe, name="edit_recipe"),
    path("create-collection/", views.create_collection, name="create_collection"),
    path(
        "edit-collection/<slug:collection_slug>/",
        views.edit_collection,
        name="edit_collection",
    ),
    path(
        "delete-collection/<slug:collection_slug>/",
        views.delete_collection,
        name="delete_collection",
    ),
]
