from django import forms
from .models import Recipe, Collection


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "collections",
            "galleries",
            "time",
            "picture",
            "ingredients",
            "instructions",
        ]
        exclude = ["user", "slug"]
        widgets = {
            "collections": forms.CheckboxSelectMultiple(),
            "galleries": forms.CheckboxSelectMultiple(),
            "ingredients": forms.Textarea(
                attrs={"rows": 8, "placeholder": "Un ingrédient par ligne"}
            ),
            "instructions": forms.Textarea(
                attrs={"rows": 12, "placeholder": "Décrivez les étapes de préparation"}
            ),
        }
        labels = {
            "title": "Nom de la recette",
            "collections": "Collections",
            "galleries": "Galleries",
            "time": "Temps de préparation (minutes)",
            "picture": "Photo",
            "ingredients": "Ingrédients",
            "instructions": "Instructions",
        }


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ["name", "description", "image"]
        exclude = ["user", "slug"]
        widgets = {
            "description": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Description de la collection"}
            ),
        }
        labels = {
            "name": "Nom de la collection",
            "description": "Description",
            "image": "Image",
        }
