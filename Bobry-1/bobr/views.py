from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User

# Upewnij się, że kropka przed models i serializers jest!
from .models import Bobr, Zeremie, GatunekDrzewa, Obserwacja
from .serializers import (
    BobrSerializer, 
    ZeremieSerializer, 
    ObserwacjaSerializer, 
    UserRegisterSerializer
)

# ---------------------------------------------------------
# TU ZACZYNAJĄ SIĘ WIDOKI - SPRAWDŹ CZY TO MASZ
# ---------------------------------------------------------

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

class BobrViewSet(viewsets.ModelViewSet):
    queryset = Bobr.objects.all()
    serializer_class = BobrSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def grubaski(self, request):
        min_waga = request.query_params.get('min_waga', 15)
        grube_bobry = Bobr.objects.filter(waga__gte=min_waga)
        serializer = self.get_serializer(grube_bobry, many=True)
        return Response(serializer.data)

class ZeremieViewSet(viewsets.ModelViewSet):
    queryset = Zeremie.objects.all()
    serializer_class = ZeremieSerializer
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def raport_remontowy(self, request):
        do_remontu = Zeremie.objects.filter(czy_wymaga_remontu=True).count()
        return Response({
            "status": "Raport Inżynierski",
            "tamy_do_naprawy": do_remontu,
            "komentarz": "Do roboty!" if do_remontu > 0 else "Luksus."
        })

class ObserwacjaViewSet(viewsets.ModelViewSet):
    queryset = Obserwacja.objects.all()
    serializer_class = ObserwacjaSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)