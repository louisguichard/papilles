from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Check if the slug exists
            counter = 1
            original_slug = self.slug
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    categories = models.ManyToManyField(
        Category,
        related_name="recipes",
        blank=True,
    )
    time = models.IntegerField(blank=True, null=True)
    picture = models.ImageField(upload_to="recipes/", blank=True, null=True)
    ingredients = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
            # Check if the slug exists
            counter = 1
            original_slug = self.slug
            while Recipe.objects.filter(slug=self.slug).exists():
                counter += 1
                self.slug = f"{original_slug}-{counter}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
