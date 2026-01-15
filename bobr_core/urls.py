"""
URL configuration for bobr_core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token # Logowanie (daje token)
from bobry.views import BobrViewSet, ZeremieViewSet, ObserwacjaViewSet, RegisterView # Import widoków

# Router automatycznie tworzy ścieżki dla ViewSetów (CRUD)
router = DefaultRouter()
router.register(r'bobry', BobrViewSet)
router.register(r'zeremie', ZeremieViewSet)
router.register(r'obserwacje', ObserwacjaViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Główne API (bobry, tamy, obserwacje)
    path('api/', include(router.urls)),
    
    # Logowanie: wysyłasz login/hasło -> dostajesz token
    path('api-token-auth/', obtain_auth_token),
    
    # Rejestracja: wysyłasz login/hasło/email -> tworzy konto
    path('register/', RegisterView.as_view(), name='auth_register'),
]