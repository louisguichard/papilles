from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    categories = models.ManyToManyField(
        Category,
        related_name="recipes",
        blank=True,
    )
    time = models.IntegerField(blank=True, null=True)
    picture = models.ImageField(upload_to="recipes/", blank=True, null=True)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    def __str__(self):
        return self.title
