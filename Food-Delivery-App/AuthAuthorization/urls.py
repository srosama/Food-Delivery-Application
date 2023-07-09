from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', view=Login.as_view(), name='login'),
    path('singup/', view=Regsterion.as_view(), name='singup'),

    path('reset_password/', PasswordResetView.as_view(), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name="password_reset_done"),
    path('rest/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
