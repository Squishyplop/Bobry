from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, GatunekDrzewa, Obserwacja
from datetime import date

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class GatunekDrzewaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatunekDrzewa
        fields = '__all__'

class BobrSerializer(serializers.ModelSerializer):
    wiek_ludzki = serializers.SerializerMethodField()

    class Meta:
        model = Bobr
        fields = ['id', 'imie', 'data_urodzenia', 'waga', 'wiek_ludzki']

    def get_wiek_ludzki(self, obj):
        if obj.data_urodzenia:
            dni = (date.today() - obj.data_urodzenia).days
            return int(dni / 365 * 3)
        return 0

    def validate_imie(self, value):
        zakazane_slowa = ["Siusiak", "Głupek", "Admin"]
        if value in zakazane_slowa:
            raise serializers.ValidationError(f"Imię '{value}' jest obraźliwe lub zastrzeżone!")
        return value

    def validate(self, data):
        if data['data_urodzenia'] == date.today() and data['waga'] > 5:
            raise serializers.ValidationError("Noworodek bobra nie może ważyć więcej niż 5 kg!")
        return data

class ZeremieSerializer(serializers.ModelSerializer):
    budowniczy_info = serializers.StringRelatedField(source='budowniczy', read_only=True)
    budowniczy_id = serializers.PrimaryKeyRelatedField(
        queryset=Bobr.objects.all(), source='budowniczy', write_only=True
    )

    class Meta:
        model = Zeremie
        fields = ['id', 'lokalizacja', 'czy_wymaga_remontu', 'budowniczy_info', 'budowniczy_id']

class ObserwacjaSerializer(serializers.ModelSerializer):
    autor = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Obserwacja
        fields = ['id', 'autor', 'opis', 'data_zgloszenia']