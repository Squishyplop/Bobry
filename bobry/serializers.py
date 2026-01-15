from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, Obserwacja

# Serializer do rejestracji użytkowników
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user

# Serializery dla naszych bobrów
class BobrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bobr
        fields = '__all__'

class ZeremieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Zeremie
        fields = '__all__'

class ObserwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obserwacja
        fields = '__all__'