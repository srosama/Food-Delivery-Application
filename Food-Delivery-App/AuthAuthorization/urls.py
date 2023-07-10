from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', view=Login.as_view(), name='login'),
    path('logout/', view=Logout.as_view(), name='logout'),
    path('singup/', view=RegsterionAPI.as_view(), name='singup'),
    path('singup-details/', view=BasicRegsterion.as_view(), name='singup-details'),
    
    #Auth the user
    path('reset_password/', PasswordResetView.as_view(), name="reset_password"),
    #The email have been sent
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_sent.html'), name="password_reset_done"),
    #Change Password 
    path('rest/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    #Password Changed
    path('reset_password_complete/', PasswordResetCompleteView.as_view(), name="password_reset_complete"),

    #User Account Details
    path('account/', userMainAccount, name='userMain')
]
