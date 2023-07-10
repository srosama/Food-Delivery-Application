from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return func(request, *args, **kwargs)
    
    return wrapper_func

def allowed_users(allowed_roles=[]):
    def decorator(func):
        def wrapper_func(request, *args, **kwargs):
            group =None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group in allowed_roles:            
                return func(request, *args, **kwargs)
            else:
                return HttpResponse("You are not authorized")
        return wrapper_func           
    return decorator 




#Don't do this in real project!
def admin_only(func):
    def wrapper_func(request, *args, **kwargs):
        group =None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':            
            return redirect('userMain')
        if group == 'admin':
            return func(request, *args, **kwargs)
        else:
            return HttpResponse("You are not authorized")
    return wrapper_func           

