from django.shortcuts import render
#Views
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


#resturantsList Show all resturants in the database
class resturantsList(ListView):
    def get(self, request):
        return render(request,'resturants/resturantsList.html')