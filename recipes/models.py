from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Gallery(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField()
    image = models.ImageField(upload_to="galleries/", blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="collections/", blank=True, null=True)
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="collections",
        null=True,
        blank=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Check if the slug exists for this user's collections
            counter = 1
            original_slug = self.slug
            while Collection.objects.filter(slug=self.slug, user=self.user).exists():
                counter += 1
                self.slug = f"{original_slug}-{counter}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="recipes", null=True, blank=True
    )
    collections = models.ManyToManyField(
        Collection,
        related_name="recipes",
        blank=True,
    )
    galleries = models.ManyToManyField(
        Gallery,
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
            # Check if the slug exists for this user's recipes
            counter = 1
            original_slug = self.slug
            while Recipe.objects.filter(slug=self.slug, user=self.user).exists():
                counter += 1
                self.slug = f"{original_slug}-{counter}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
