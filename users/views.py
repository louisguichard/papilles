from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from recipes.models import Collection


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserRegistrationForm()

    return render(request, "users/register.html", {"form": form})


def profile(request):
    collections = Collection.objects.filter(user=request.user)[
        :4
    ]  # Show just the first 4 collections
    return render(request, "users/profile.html", {"collections": collections})


def logout_view(request):
    logout(request)
    # Get the referring page or use home as fallback
    referer = request.META.get("HTTP_REFERER")
    if referer:
        return HttpResponseRedirect(referer)
    else:
        return redirect("home")
