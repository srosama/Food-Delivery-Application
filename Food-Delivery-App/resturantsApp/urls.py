from django.urls import path
from .views import *


urlpatterns = [

    path('resturant/<id>', resturantsSingle.as_view(), name='resturantsSingle'),
    path('resturants/', resturantsList.as_view(), name='resturantslist'),
    path('resturant-main/dashboard', Main_dashboard.as_view(), name='main_dashboard'),

    #Add menu items
    path('resturant-menu/add-menu-item', add_new_menu.as_view(), name='add_new_menu'),


    
    #Tests
    path('resturant/testNav', navbarCool,name='test'),
]


