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
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from bobry.pages import index, login_page, logout_page, register_page, feed_page, add_bobr_page, admin_panel_page, add_zeremie_page

from bobry.views import (
    BobrViewSet,
    ZeremieViewSet,
    ObserwacjaViewSet,
    GatunekDrzewaViewSet,
    RegisterView,
    UserProfileViewSet
)

# CRUD?
router = DefaultRouter()
router.register(r'bobry', BobrViewSet)
router.register(r'zeremia', ZeremieViewSet)
router.register(r'obserwacje', ObserwacjaViewSet)
router.register(r'drzewa', GatunekDrzewaViewSet)

router.register(r'profile', UserProfileViewSet)

urlpatterns = [
    path("", index, name="index"),
    path("login/", login_page, name="login"),
    path("logout/", logout_page, name="logout"),
    path("register/", register_page, name="register"),
    path("feed/", feed_page, name="feed"),

    path("bobry/add/", add_bobr_page, name="add_bobr"),
    path("admin-panel/", admin_panel_page, name="admin_panel"),

    path("zeremia/add/", add_zeremie_page, name="add_zeremie"),

    path('admin/', admin.site.urls),

    # API
    path('api/', include(router.urls)),
    path('api-token-auth/', obtain_auth_token),

    # API rejestracja (inna nazwa!)
    path('api/register/', RegisterView.as_view(), name='api_register'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
