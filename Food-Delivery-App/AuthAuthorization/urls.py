from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('login/', view=Login.as_view(), name='login'),
    path('singup/', view=Regsterion.as_view(), name='singup'),
    path('login/api', view=LoginApi.as_view(), name='api'),
]
