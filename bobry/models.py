from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    RANGA_CHOICES = [
        ('BB', 'Bóbr'),
        ('SB', 'SuperBóbr'),
        ('KR', 'Król Bóbr'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ranga = models.CharField(max_length=2, choices=RANGA_CHOICES, default='BB')

    def __str__(self):
        return f"{self.user.username} – {self.get_ranga_display()}"


class GatunekDrzewa(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa


class Bobr(models.Model):
    imie = models.CharField(max_length=50)
    data_urodzenia = models.DateField(null=True, blank=True)
    waga = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.imie} ({self.waga}kg)"


class Zeremie(models.Model):
    lokalizacja = models.CharField(max_length=200)
    czy_wymaga_remontu = models.BooleanField(default=False)

    budowniczy = models.ForeignKey(
        Bobr,
        on_delete=models.CASCADE,
        related_name='zeremia'
    )

    gatunek_drzewa = models.ForeignKey(
        GatunekDrzewa,
        on_delete=models.PROTECT,
        related_name='zeremia'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Żeremie ({self.gatunek_drzewa}) – {self.lokalizacja}"


class Obserwacja(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    opis = models.TextField()
    data_zgloszenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Zgłoszenie od {self.autor}"


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('BOBR', 'Dodano bobra'),
        ('OBS', 'Dodano obserwację'),
        ('ZER', 'Zbudowano żeremie'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=10, choices=ACTIVITY_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    bobr = models.ForeignKey(Bobr, null=True, blank=True, on_delete=models.CASCADE)
    obserwacja = models.ForeignKey(Obserwacja, null=True, blank=True, on_delete=models.CASCADE)
    zeremie = models.ForeignKey(Zeremie, null=True, blank=True, on_delete=models.CASCADE)
