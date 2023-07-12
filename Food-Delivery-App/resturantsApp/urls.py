from django.urls import path
from .views import resturantsList

urlpatterns = [
    path('resturants/', resturantsList.as_view(), name='resturantslist'),
]
