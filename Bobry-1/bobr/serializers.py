from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, GatunekDrzewa, Obserwacja
from datetime import date

# 
# 1. SERIALIZER UŻYTKOWNIKA (Do Rejestracji)
# 
class UserRegisterSerializer(serializers.ModelSerializer):
    # Hasło musi być ukryte przy odczycie (write_only)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    # Funkcja tworząca użytkownika (zaszyfrowanie hasła)
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

# 
# 2. SERIALIZER GATUNKU DRZEWA (Słownik)
# 
class GatunekDrzewaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatunekDrzewa
        fields = '__all__'

# 
# 3. SERIALIZER BOBRA (Główny bohater)
# 
class BobrSerializer(serializers.ModelSerializer):
    # Możemy dodać pole wyliczane, którego nie ma w bazie
    wiek_ludzki = serializers.SerializerMethodField()

    class Meta:
        model = Bobr
        fields = ['id', 'imie', 'data_urodzenia', 'waga', 'wiek_ludzki']

    # Logika wyliczania pola (nie zapisujemy tego w bazie, tylko wyświetlamy)
    def get_wiek_ludzki(self, obj):
        if obj.data_urodzenia:
            dni = (date.today() - obj.data_urodzenia).days
            return int(dni / 365 * 3) # Przelicznik: 1 rok bobra to ok. 3 lata ludzkie
        return 0

    # IDIOTOODPORNOŚĆ - Walidacja konkretnego pola
    def validate_imie(self, value):
        zakazane_slowa = ["Siusiak", "Głupek", "Admin"]
        if value in zakazane_slowa:
            raise serializers.ValidationError(f"Imię '{value}' jest obraźliwe lub zastrzeżone!")
        return value

    # IDIOTOODPORNOŚĆ - Walidacja wielu pól na raz
    def validate(self, data):
        # Sprawdźmy, czy waga jest adekwatna do wieku (uproszczone)
        # Jeśli data urodzenia jest dzisiaj (noworodek), nie może ważyć 30 kg
        if data['data_urodzenia'] == date.today() and data['waga'] > 5:
            raise serializers.ValidationError("Noworodek bobra nie może ważyć więcej niż 5 kg!")
        return data

# 
# 4. SERIALIZER ŻEREMIA (Tamy)
# 
class ZeremieSerializer(serializers.ModelSerializer):
    # Zamiast ID bobra, chcemy widzieć jego imię przy odczycie?
    # StringRelatedField wyświetli to, co zwraca metoda __str__ w modelu Bobra
    budowniczy_info = serializers.StringRelatedField(source='budowniczy', read_only=True)
    
    # Ale do zapisu nadal potrzebujemy ID
    budowniczy_id = serializers.PrimaryKeyRelatedField(
        queryset=Bobr.objects.all(), source='budowniczy', write_only=True
    )

    class Meta:
        model = Zeremie
        fields = ['id', 'lokalizacja', 'czy_wymaga_remontu', 'budowniczy_info', 'budowniczy_id']

# 
# 5. SERIALIZER OBSERWACJI (Zgłoszenia użytkowników)
# 
class ObserwacjaSerializer(serializers.ModelSerializer):
    # Autora ustawimy automatycznie z zalogowanego usera, więc jest tylko do odczytu
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Obserwacja
        fields = ['id', 'autor', 'opis', 'data_zgloszenia']