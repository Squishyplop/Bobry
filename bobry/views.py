from django.shortcuts import render
from rest_framework import viewsets, generics, permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import Bobr, Zeremie, Obserwacja, GatunekDrzewa, UserProfile, Activity
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import BobrSerializer, ZeremieSerializer, ObserwacjaSerializer, RegisterSerializer, \
    GatunekDrzewaSerializer, UserProfileSerializer
from itertools import chain


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer


class BobrViewSet(viewsets.ModelViewSet):
    queryset = Bobr.objects.all()
    serializer_class = BobrSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def grubaski(self, request):
        min_waga = float(request.query_params.get('min_waga', 15))
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
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def raport_remontowy(self, request):
        do_remontu = Zeremie.objects.filter(czy_wymaga_remontu=True).count()
        return Response({
            "status": "Raport Inżynierski",
            "tamy_do_naprawy": do_remontu,
            "komentarz": "Do roboty!" if do_remontu > 0 else "Tu jest jakby luksusowo."
        })


class ObserwacjaViewSet(viewsets.ModelViewSet):
    queryset = Obserwacja.objects.all().order_by('-data_zgloszenia')
    serializer_class = ObserwacjaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)


class GatunekDrzewaViewSet(viewsets.ModelViewSet):
    queryset = GatunekDrzewa.objects.all()
    serializer_class = GatunekDrzewaSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    @action(detail=True, methods=['post'])
    def ustaw_range(self, request, pk=None):
        profile = self.get_object()
        nowa_ranga = request.data.get('ranga', '').upper()

        if nowa_ranga not in dict(UserProfile.RANGA_CHOICES):
            return Response({"error": "Nieprawidłowa ranga."}, status=400)

        profile.ranga = nowa_ranga
        profile.save()
        return Response({
            "status": "Ranga zmieniona",
            "nowa_ranga": profile.get_ranga_display()
        })


def feed(request):
    bobry = Bobr.objects.all()
    obserwacje = Obserwacja.objects.all()

    print("BOBRY:", bobry.count())
    print("OBSERWACJE:", obserwacje.count())

    feed_items = sorted(
        chain(bobry, obserwacje),
        key=lambda x: x.created_at if hasattr(x, 'created_at') else x.data_zgloszenia,
        reverse=True
    )

    print("FEED ITEMS:", len(feed_items))

    return render(request, 'feed.html', {
        'feed_items': feed_items
    })