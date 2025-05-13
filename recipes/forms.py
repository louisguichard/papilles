from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "collections",
            "time",
            "picture",
            "ingredients",
            "instructions",
        ]
        exclude = ["user", "slug"]
        widgets = {
            "collections": forms.CheckboxSelectMultiple(),
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
            "time": "Temps de préparation (minutes)",
            "picture": "Photo",
            "ingredients": "Ingrédients",
            "instructions": "Instructions",
        }
