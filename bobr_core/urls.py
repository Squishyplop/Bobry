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
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from bobry.views import (
    BobrViewSet, 
    ZeremieViewSet, 
    ObserwacjaViewSet, 
    GatunekDrzewaViewSet, 
    RegisterView
)

# CRUD?
router = DefaultRouter()
router.register(r'bobry', BobrViewSet)
router.register(r'zeremia', ZeremieViewSet)
router.register(r'obserwacje', ObserwacjaViewSet)
router.register(r'drzewa', GatunekDrzewaViewSet) 


urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Główne API
    path('api/', include(router.urls)),
    
    # Login i hasło - token
    path('api-token-auth/', obtain_auth_token),
    
    # login, hasło, email - konto
    path('api/register/', RegisterView.as_view(), name='auth_register'),
]