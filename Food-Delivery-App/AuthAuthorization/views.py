from django.shortcuts import render
from django.views.generic import View


class Login(View):
    def get(self, req):
        return render(req, 'auth/login.html')