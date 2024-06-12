
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from ..models import *

def show_admin_panel(request):
    check = perform_auth_check(request)
    if check != True:
        return check
    users = Profile.objects.all()
    admin_context = {
        "users": users
    }
    return render(request=request, template_name='musicmix/adminpanel.html', context=admin_context)
    

def perform_auth_check(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        raise PermissionDenied()
    return True
