from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, Obserwacja, GatunekDrzewa, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # pokazuje username
    ranga_display = serializers.CharField(source='get_ranga_display', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'ranga', 'ranga_display']


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


class BobrSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bobr
        fields = '__all__'
        read_only_fields = ('user',)  # user ustawiasz w perform_create

    def validate_waga(self, value):
        if value <= 0:
            raise serializers.ValidationError("Waga musi być większa od 0.")
        if value > 200:
            raise serializers.ValidationError("Waga jest nienaturalnie wysoka.")
        return value

    def validate_data_urodzenia(self, value):
        if value is None:
            return value
        if value > timezone.now().date():
            raise serializers.ValidationError("Data urodzenia nie może być z przyszłości.")
        return value


class ZeremieSerializer(serializers.ModelSerializer):
    gatunek_drzewa_nazwa = serializers.CharField(
        source='gatunek_drzewa.nazwa',
        read_only=True
    )

    class Meta:
        model = Zeremie
        fields = '__all__'

class ObserwacjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Obserwacja
        fields = '__all__'


class GatunekDrzewaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GatunekDrzewa
        fields = '__all__'
