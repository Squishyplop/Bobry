from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from .models import Bobr, Zeremie
from .serializers import BobrSerializer

class BobrViewSet(viewsets.ModelViewSet):
    queryset = Bobr.objects.all()
    serializer_class = BobrSerializer
    # Domyślne zabezpieczenie:
    permission_classes = [IsAuthenticated] 

    # 
    # ENDPOINT POZA SCHEMATEM 1: Filtracja (Grube Bobry)
    # URL: /api/bobry/grubaski/?min_waga=20
    # 
    @action(detail=False, methods=['get'])
    def grubaski(self, request):
        min_waga = request.query_params.get('min_waga', 15)
        # Logika: Filtrujemy bobry cięższe niż X
        grube_bobry = Bobr.objects.filter(waga__gte=min_waga)
        serializer = self.get_serializer(grube_bobry, many=True)
        return Response(serializer.data)

class ZeremieViewSet(viewsets.ModelViewSet):
    queryset = Zeremie.objects.all()
    # Tylko Admin może majstrować przy tamach!
    permission_classes = [IsAdminUser] 
    
    # 
    # ENDPOINT POZA SCHEMATEM 2: Raport (Statystyka)
    # URL: /api/zeremie/raport_remontowy/
    # 
    @action(detail=False, methods=['get'])
    def raport_remontowy(self, request):
        # Logika: Policz ile tam wymaga remontu
        do_remontu = Zeremie.objects.filter(czy_wymaga_remontu=True).count()
        return Response({
            "status": "Raport Inżynierski",
            "tamy_do_naprawy": do_remontu,
            "komentarz": "Bobry muszą wziąć się do roboty." if do_remontu > 0 else "Jest super."
        })