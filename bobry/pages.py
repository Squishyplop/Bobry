from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile, Bobr, Obserwacja, Zeremie, Activity, GatunekDrzewa
from django.contrib.auth.decorators import login_required, user_passes_test
from itertools import chain
from django.shortcuts import get_object_or_404


def index(request):
    return render(request, "index.html")


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        messages.error(request, "Błędny login lub hasło.")
    return render(request, "login.html")


def logout_page(request):
    logout(request)
    return redirect("index")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if not username or not password:
            messages.error(request, "Username i hasło są wymagane.")
            return render(request, "register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Taki użytkownik już istnieje.")
            return render(request, "register.html")

        User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Konto utworzone. Możesz się zalogować.")
        return redirect("login")

    return render(request, "register.html")

from django.contrib.auth.decorators import login_required
from .models import Obserwacja


@login_required
def feed_page(request):
    activities = (
        Activity.objects
        .select_related(
            "user",
            "bobr",
            "obserwacja",
        )
        .order_by("-created_at")
    )

    return render(request, "feed.html", {
        "activities": activities
    })

@login_required
def add_bobr_page(request):
    if request.method == "POST":
        imie = request.POST.get("imie", "").strip()
        waga = request.POST.get("waga", "").strip()
        data_urodzenia = request.POST.get("data_urodzenia", "").strip() or None

        if not imie:
            messages.error(request, "Imię jest wymagane.")
            return render(request, "add_bobr.html")

        try:
            waga_val = float(waga)
        except ValueError:
            messages.error(request, "Waga musi być liczbą.")
            return render(request, "add_bobr.html")

        if waga_val <= 0:
            messages.error(request, "Waga musi być większa od 0.")
            return render(request, "add_bobr.html")

        Bobr.objects.create(
            imie=imie,
            waga=waga_val,
            data_urodzenia=data_urodzenia,
            user=request.user
        )

        messages.success(request, "Bóbr dodany!")
        return redirect("feed")

    return render(request, "add_bobr.html")

def is_admin(user):
    return user.is_staff

@login_required
@user_passes_test(is_admin)
def admin_panel_page(request):
    profiles = UserProfile.objects.select_related("user").all()
    query = request.GET.get("q", "").strip()
    if query:
        profiles = profiles.filter(user__username__icontains=query)

    if request.method == "POST":
        profile_id = request.POST.get("profile_id")
        new_rank = request.POST.get("ranga")

        profile = UserProfile.objects.get(id=profile_id)
        profile.ranga = new_rank
        profile.save()

    return render(
        request,
        "admin_panel.html",
        {
            "profiles": profiles,
            "query": query,
            "rangi": UserProfile.RANGA_CHOICES,
        }
    )

@login_required
def add_zeremie_page(request):
    bobry = Bobr.objects.all()
    drzewa = GatunekDrzewa.objects.all()

    if request.method == "POST":
        lokalizacja = request.POST.get("lokalizacja", "").strip()
        budowniczy_id = request.POST.get("budowniczy")
        drzewo_id = request.POST.get("gatunek_drzewa")
        czy_wymaga_remontu = bool(request.POST.get("czy_wymaga_remontu"))

        if not lokalizacja or not drzewo_id or not budowniczy_id:
            messages.error(
                request,
                "Lokalizacja, bóbr i gatunek drzewa są wymagane."
            )
            return render(request, "add_zeremie.html", {
                "bobry": bobry,
                "drzewa": drzewa
            })

        budowniczy = get_object_or_404(Bobr, id=budowniczy_id)
        drzewo = get_object_or_404(GatunekDrzewa, id=drzewo_id)

        Zeremie.objects.create(
            lokalizacja=lokalizacja,
            budowniczy=budowniczy,
            gatunek_drzewa=drzewo,
            czy_wymaga_remontu=czy_wymaga_remontu
        )

        messages.success(request, "Żeremie dodane!")
        return redirect("feed")

    return render(request, "add_zeremie.html", {
        "bobry": bobry,
        "drzewa": drzewa
    })
