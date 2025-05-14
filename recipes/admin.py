from django.contrib import admin
from .models import Collection, Recipe, Gallery

# Register your models here.
admin.site.register(Gallery)
admin.site.register(Collection)
admin.site.register(Recipe)
