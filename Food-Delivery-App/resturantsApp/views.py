from django.shortcuts import render
#Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from AuthAuthorization.models import *


#resturantsList Show all resturants in the database
class resturantsList(ListView):
    def get(self, request):
        resturants = AddNewRestaurant.objects.all()
        return render(request,'resturants/resturantsList.html', {'resturants': resturants})
