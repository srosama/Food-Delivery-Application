from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import View
from .models import User
import jwt, datetime
from django.contrib.auth import authenticate, login, logout 

#Api Rest
from rest_framework.views import APIView 
from rest_framework.exceptions import AuthenticationFailed 
from .serializers import UserSer
from rest_framework.response import Response

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
class LoginApi(APIView):
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


