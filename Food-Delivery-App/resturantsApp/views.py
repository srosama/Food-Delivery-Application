from django.shortcuts import render
#Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from AuthAuthorization.models import *


#resturantsList Show all resturants in the database
class resturantsList(ListView):
    def get(self, request):
        resturants = AddNewRestaurantV2.objects.all()
        return render(request,'resturants/resturantsList.html', {'resturants': resturants})


class Main_dashboard(TemplateView):
    def get(self, request):
        user = request.user
        logo = AddNewRestaurantV2.objects.get(user=user)
        resturants = AddNewRestaurantV2.objects.all()
        context = {'logo': logo,'resturants': resturants}
        return render(request,'resturants/dashboard/base-Dashboard.html',context=context)


class resturantsSingle(TemplateView):
    def get(self, request, id):
        single_restaurant = AddNewRestaurantV2.objects.get(id_Restaurant=id)
        context = {'restaurantData': single_restaurant}
        return render(request, 'resturants/resturantsSingle.html', context=context)

#Tests
def navbarCool(request):
    user = request.user
    logo = AddNewRestaurantV2.objects.get(user=user)

    return render(request,'components/resturants/navbar.html', {'logo': logo})

