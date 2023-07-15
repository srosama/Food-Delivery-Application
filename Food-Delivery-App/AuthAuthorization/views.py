from typing import Any
from django.shortcuts import render, redirect

#Auth
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from rest_framework.exceptions import AuthenticationFailed 

#Rest Framwork
import jwt, datetime
from .serializers import UserSer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import default_token_generator

#Databases
from .models import User, AddNewRestaurantV2, testImg
from .models import User, customerAccountDetails

#Decoretors
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from .decorators import allowed_users, admin_only, unauthenticated_user
#Views
from rest_framework.views import APIView 
from django.views.generic import View
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
from django.views.generic.base import TemplateView

#Froms
from .forms import PasswordResetForm, SetPasswordForm, addFormT, testImgsForm
from urllib.parse import urlparse, urlunparse
from django.conf import settings

#User Creation Form
from django.contrib.auth.forms import UserCreationForm

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.http import HttpResponse 
from django.contrib.auth.models import Group




    

def test(request):
    if request.method == 'POST':
        name = request.POST['name']
        img = request.FILES['img']
        testimg = testImg.objects.create(name=name, testImg=img)
        testimg.save()
        return HttpResponse("save")
    return render(request, 'test.html', )



#User Account Mangment
@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userMainAccount(request):
    user_name = request.user.email
    print(user_name)
    context = {'name':user_name}
    return render(request, 'accounts/userMainpage.html',context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['restaurantsOwners'])
def addNewRestaurant(request):
    auth_user = request.user.email
    USERInster = User.objects.get(email=auth_user)

    if request.method == 'POST':
        Rname = request.POST['res-name']

        Rtime_for_delivery = request.POST['res-time_for_delivery']

        Rdescription = request.POST['res-description']

        R_priceMax = request.POST['res-Pmax']
        R_priceMin = request.POST['res-Pmin']
        R_catagory = request.POST['res-catagory']

        Rlogo = request.FILES['res-logo']
        Rbannar = request.FILES['bannars']
        
        new_restaurant = AddNewRestaurantV2.objects.create(
            name=Rname,
            logo=Rlogo,
            bannar_img=Rbannar,
            time_for_delivery=Rtime_for_delivery,
            description=Rdescription,
            price_Max=R_priceMax,
            price_Min=R_priceMin,
            category=R_catagory,
            user=USERInster
        )
        new_restaurant.save()
        return HttpResponse("save")

    return render(request, 'auth/restaurantsOwners/auth/restaurant-details.html' )



class Login(View):
    def get(self, req):
        return render(req, 'auth/login.html')
    
    def post(self, req):
        email = req.POST['email']
        password = req.POST['password']        

        user = authenticate(req, email=email, password=password)
        
        if user is not None:
            login(req, user)
            userDeatials = customerAccountDetails.objects.all()
            context = {"phone":userDeatials}
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

class RegsterionAPI(APIView):

    def get(self, req):
        return render(req, 'auth/singup.html')
    def post(self, req):
        where = req.POST['createAccount']    
        print(req.POST)
        if where == 'restaurant':
            return redirect('basic-restaurant-regsterion')
        elif where == 'personal':
            return redirect('singup-details')
    
        return HttpResponse(req.POST)
class RegsterionDetailsAPI(APIView):
    def get(self, req):
        return render(req, 'auth/user-details.html')

    def post(self, req):
        serilzer = UserSer(data=req.data)
        serilzer.is_valid(raise_exception=True)
        if serilzer.is_valid():
            serilzer.save()
            messages.success(req, 'You have succfully create your account')
            return redirect('home')
        else:          
            data = serilzer.errors
            messages.error(req, "You have enter bad input", extra_tags='danger')
            return Response(data)
class BasicRegsterion(TemplateView):
   #Get 
   def get(self, req):
      form = UserCreationForm()
      context = {"form":form}
      return render(req, 'auth/user-details.html', context)

   #Post     
   def post(self, req):
       fullName = req.POST['name']       
       email = req.POST['email']       
       password = req.POST['password']       
       password2 = req.POST['password2']    
       masater = [fullName, email, password,password2] 

       #Password Simple Vaildtion => Add Regix !important 
       if password != password2:
           messages.error(req, "Password Not Mattches plz check it again ".title(), extra_tags='danger')
           return redirect('singup-details')
       if len(password) < 8:
           messages.error(req, "Password Should be above 8".title(), extra_tags='danger')
           return redirect('singup-details')
       
       if User.objects.filter(email=email):
           messages.error(req, "email already in use, if this is you plz login".title(), extra_tags='danger')
           return redirect('singup-details')
       
       userSave = User.objects._create_user(email=email,password=password,fullName=fullName)

       #Add the user to the customer group
       user = User.objects.get(email=email)
       group = Group.objects.get(name="customer")
       user.groups.add(group)
       userSave.save()
       
       #After singup the user
       login(req, userSave)
       messages.success(req, "You have successfully created your account".title())
       return redirect('home')       

class BasicRestaurantRegsterion(View):
    def get(self, request):
        return render(request, 'auth/restaurantsOwners/auth/singup.html')
    def post(self, req):
       fullName = req.POST['name']       
       email = req.POST['email']       
       password = req.POST['password']       
       password2 = req.POST['password2']    

       #Password Simple Vaildtion => Add Regix !important 
       if password != password2:
           messages.error(req, "Password Not Mattches plz check it again ".title(), extra_tags='danger')
           return redirect('singup-details')
       if len(password) < 8:
           messages.error(req, "Password Should be above 8".title(), extra_tags='danger')
           return redirect('singup-details')
       
       if User.objects.filter(email=email):
           messages.error(req, "email already in use, if this is you plz login".title(), extra_tags='danger')
           return redirect('singup-details')
       
       userSave = User.objects._create_user(email=email,password=password,fullName=fullName)

       #Add the user to the customer group
       user = User.objects.get(email=email)
       group = Group.objects.get(name="restaurantsOwners")
       user.groups.add(group)
       userSave.save()
       
       #After singup the user
       login(req, userSave)
       messages.success(req, "You have successfully created your account".title())
       return redirect('addnewrstaurant')    


#Reset password
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
    template_name = "registration/password_reset_form.html"
    title = ("Password reset")
    token_generator = default_token_generator
    
    @method_decorator(csrf_protect)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        if not User.objects.filter(email=email).first():
            messages.success(request, 'Bad Email', extra_tags='danger')
            return redirect('reset_password')
        
        form = self.get_form()
        if form.is_valid():
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
            super().form_valid(form)
            messages.success(request, 'We Have Sent you a email to reset the password')
            return redirect('password_reset_done')
INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"
class PasswordResetConfirmView(PasswordContextMixin, FormView):
    form_class = SetPasswordForm
    post_reset_login = False
    post_reset_login_backend = None
    reset_url_token = "set-password"
    success_url = reverse_lazy("password_reset_complete")
    template_name = "registration/password_reset_confirm.html"
    title = _("Enter new password")
    token_generator = default_token_generator

    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        return self.render_to_response(self.get_context_data())
    
        
    def get_user(self, uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        user = form.save()
        del self.request.session[INTERNAL_RESET_SESSION_TOKEN]
        if self.post_reset_login:
            auth_login(self.request, user, self.post_reset_login_backend)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.validlink:
            context["validlink"] = True
        else:
            context.update(
                {
                    "form": None,
                    "title": _("Password reset unsuccessful"),
                    "validlink": False,
                }
            )
        return context
class PasswordResetCompleteView(PasswordContextMixin, TemplateView):
    template_name = "registration/password_reset_complete.html"
    title = _("Password reset complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["login_url"] = resolve_url(settings.LOGIN_URL)
        return context


