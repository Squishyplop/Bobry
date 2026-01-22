from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

# Funkcja walidująca (idiotoodporność dla daty)
def nie_z_przyszlosci(value):
    if value > timezone.now().date():
        raise ValidationError("Bóbr nie jest podróżnikiem w czasie! Data nie może być z przyszłości.")

# Gatunki drzew 
class GatunekDrzewa(models.Model):
    nazwa = models.CharField(max_length=50)
    kalorycznosc = models.PositiveIntegerField(help_text="Ile energii daje to drewno")

    def __str__(self):
        return self.nazwa

# Opis bubra
class Bobr(models.Model):
    imie = models.CharField(max_length=50)
    data_urodzenia = models.DateField(validators=[nie_z_przyszlosci]) # Walidacja
    waga = models.FloatField(help_text="Waga w kg") 
    
    # Idiotoodporność przy zapisie
    def clean(self):
        if self.waga < 0:
            raise ValidationError("Bóbr nie może ważyć ujemnie (anty-materia?).")

# Info o domkach bubrów
class Zeremie(models.Model):
    lokalizacja = models.CharField(max_length=100)
    budowniczy = models.ForeignKey(Bobr, on_delete=models.CASCADE, related_name='tammy')
    czy_wymaga_remontu = models.BooleanField(default=False)

# Model dla użytkownika 
class Obserwacja(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    opis = models.TextField()
    data_zgloszenia = models.DateTimeField(auto_now_add=True)