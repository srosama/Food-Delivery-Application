from django.urls import path
from .views import *
urlpatterns = [
    path('login', view=Login.as_view(), name='login')
]
