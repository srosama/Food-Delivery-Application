from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from .models import User
import jwt, datetime
from django.contrib.auth import authenticate, login, logout 
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator

#Forms
from .forms import PasswordResetForm

#Views
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect

#Api Rest
from rest_framework.views import APIView 
from rest_framework.exceptions import AuthenticationFailed 
from .serializers import UserSer
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator

class Login(View):
    def get(self, req):
        return render(req, 'auth/login.html')
    
    def post(self, req):
        email = req.POST['email']
        password = req.POST['password']        

        user = authenticate(req, email=email, password=password)
        
        if user is not None:
            login(req, user)
            messages.success(req, 'Login Sccuffule')
            return redirect('home')
        else:
            messages.success(req, 'Invaild Email Or Password',  extra_tags='danger')
            return redirect('login')
class Logout(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You Have Been Logged Out")
        return redirect('home')
class Regsterion(APIView):
    def get(self, req):
        return render(req, 'auth/singup.html')
    def post(self, req):
        serilzer = UserSer(data=req.data)
        serilzer.is_valid(raise_exception=True)
        serilzer.save()
        
        return Response(serilzer.data)
    def post(self, req):
        email = req.data['email']
        password = req.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('bAD LOGIN')
        
        if not user.check_password(password):
            raise AuthenticationFailed('Incoorected password')
        
        payload = {
            'id':user.id,
            'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret' , algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            "jwt":token
        }

        return response




class PasswordContextMixin:
    extra_context = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {"title": self.title, "subtitle": None, **(self.extra_context or {})}
        )
        return context


class PasswordResetView(PasswordContextMixin, FormView):
    email_template_name = "registration/password_reset_email.html"
    extra_email_context = None
    form_class = PasswordResetForm
    from_email = None
    html_email_template_name = None
    subject_template_name = "registration/password_reset_subject.txt"
    success_url = reverse_lazy("password_reset_done")
    template_name = "accounts/password_reset.html"
    title = ("Password reset")
    token_generator = default_token_generator

    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        opts = {
            "use_https": self.request.is_secure(),
            "token_generator": self.token_generator,
            "from_email": self.from_email,
            "email_template_name": self.email_template_name,
            "subject_template_name": self.subject_template_name,
            "request": self.request,
            "html_email_template_name": self.html_email_template_name,
            "extra_email_context": self.extra_email_context,
        }
        form.save(**opts)
        return super().form_valid(form)
    
    def post(self,request):
        return redirect('login')