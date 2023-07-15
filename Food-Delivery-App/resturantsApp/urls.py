from django.urls import path
from .views import *


urlpatterns = [

    path('resturant/<id>', resturantsSingle.as_view(), name='resturantslist'),
    path('resturants/', resturantsList.as_view(), name='resturantslist'),
    path('resturant/dashboard', Main_dashboard.as_view(), name='main_dashboard'),

    #Tests
    path('resturant/testNav', navbarCool,name='test'),
]


