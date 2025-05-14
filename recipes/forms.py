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
            "variations",
            "nutrition",
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
            "variations": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Variantes possibles de la recette"}
            ),
            "nutrition": forms.Textarea(
                attrs={"rows": 6, "placeholder": "Informations nutritionnelles"}
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
            "variations": "Variantes",
            "nutrition": "Nutrition",
        }

    def __init__(self, user=None, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        # Filter collections to only show user's own collections
        if user:
            self.fields["collections"].queryset = Collection.objects.filter(user=user)


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
