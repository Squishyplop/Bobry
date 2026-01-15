from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class GatunekDrzewa(models.Model):
    nazwa = models.CharField(max_length=100)

    def __str__(self):
        return self.nazwa

class Bobr(models.Model):
    imie = models.CharField(max_length=50)
    data_urodzenia = models.DateField(null=True, blank=True)
    waga = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.imie} ({self.waga}kg)"

class Zeremie(models.Model):
    lokalizacja = models.CharField(max_length=200)
    czy_wymaga_remontu = models.BooleanField(default=False)
    budowniczy = models.ForeignKey(Bobr, on_delete=models.CASCADE, related_name='zeremia')

    def __str__(self):
        return f"Tama w: {self.lokalizacja}"

class Obserwacja(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    opis = models.TextField()
    data_zgloszenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Zgłoszenie od {self.autor}"