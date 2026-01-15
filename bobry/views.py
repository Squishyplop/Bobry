from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, Obserwacja
# Tutaj była literówka, teraz importujemy poprawną nazwę:
from .serializers import BobrSerializer, ZeremieSerializer, ObserwacjaSerializer, RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class BobrViewSet(viewsets.ModelViewSet):
    queryset = Bobr.objects.all()
    serializer_class = BobrSerializer

class ZeremieViewSet(viewsets.ModelViewSet):
    queryset = Zeremie.objects.all()
    serializer_class = ZeremieSerializer

class ObserwacjaViewSet(viewsets.ModelViewSet):
    queryset = Obserwacja.objects.all()
    serializer_class = ObserwacjaSerializer