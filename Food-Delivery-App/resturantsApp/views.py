from django.shortcuts import render
#Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from AuthAuthorization.models import AddRestaurant


#resturantsList Show all resturants in the database
class resturantsList(ListView):
    def get(self, request):
        resturants = AddRestaurant.objects.all()
        return render(request,'resturants/resturantsList.html', {'resturants': resturants})
