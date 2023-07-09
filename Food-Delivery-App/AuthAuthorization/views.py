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
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework.views import APIView 
from rest_framework.exceptions import AuthenticationFailed 
from .serializers import UserSer
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
#Databases
from .models import User
#Decoretors
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
#Views
from django.views.generic.edit import FormView
from django.views.decorators.csrf import csrf_protect
#Froms
from .forms import PasswordResetForm, SetPasswordForm
from urllib.parse import urlparse, urlunparse
from django.conf import settings

# Avoid shadowing the login() and logout() views below.
from django.contrib.auth import REDIRECT_FIELD_NAME, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme, urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView


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
