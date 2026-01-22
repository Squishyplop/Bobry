from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, Obserwacja, GatunekDrzewa
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BobrSerializer, ZeremieSerializer, ObserwacjaSerializer, RegisterSerializer, GatunekDrzewaSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class BobrViewSet(viewsets.ModelViewSet):
    queryset = Bobr.objects.all()
    serializer_class = BobrSerializer

    @action(detail=False, methods=['get'])
    def grubaski(self, request):
        min_waga = request.query_params.get('min_waga', 15)
        grube_bobry = Bobr.objects.filter(waga__gte=min_waga)
        serializer = self.get_serializer(grube_bobry, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statystyki(self, request):
        liczba_bobrow = Bobr.objects.count()
        liczba_zeremi = Zeremie.objects.count()
        liczba_drzew = GatunekDrzewa.objects.count()
        
        return Response({
            "liczba_bobrow": liczba_bobrow,
            "liczba_zeremi": liczba_zeremi,
            "liczba_gatunkow_drzew": liczba_drzew,
            "info": "Statystyki wygenerowane pomyślnie"
        })

class ZeremieViewSet(viewsets.ModelViewSet):
    queryset = Zeremie.objects.all()
    serializer_class = ZeremieSerializer
    
    @action(detail=False, methods=['get'])
    def raport_remontowy(self, request):
        do_remontu = Zeremie.objects.filter(czy_wymaga_remontu=True).count()
        return Response({
            "status": "Raport Inżynierski",
            "tamy_do_naprawy": do_remontu,
            "komentarz": "Do roboty!" if do_remontu > 0 else "Tu jest jakby luksusowo."
        })

class ObserwacjaViewSet(viewsets.ModelViewSet):
    queryset = Obserwacja.objects.all()
    serializer_class = ObserwacjaSerializer

class GatunekDrzewaViewSet(viewsets.ModelViewSet):
    queryset = GatunekDrzewa.objects.all()
    serializer_class = GatunekDrzewaSerializer