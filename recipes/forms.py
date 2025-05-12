from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "categories",
            "time",
            "picture",
            "ingredients",
            "instructions",
        ]
        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
            "ingredients": forms.Textarea(
                attrs={"rows": 8, "placeholder": "Un ingrédient par ligne"}
            ),
            "instructions": forms.Textarea(
                attrs={"rows": 12, "placeholder": "Décrivez les étapes de préparation"}
            ),
        }
        labels = {
            "title": "Nom de la recette",
            "categories": "Catégories",
            "time": "Temps de préparation (minutes)",
            "picture": "Photo",
            "ingredients": "Ingrédients",
            "instructions": "Instructions",
        }
