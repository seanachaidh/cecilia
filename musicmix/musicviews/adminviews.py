
from django.shortcuts import redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from ..forms import UserCreationForm
from ..models import *
from random import randint

def show_admin_panel(request):
    check = perform_auth_check(request)
    if check != True:
        return check
    users = Profile.objects.all()
    admin_context = {
        "users": users
    }
    return render(request=request, template_name='musicmix/adminpanel.html', context=admin_context)
    

def add_user(request):
    check = perform_auth_check(request)
    if not check:
        return check
    if request.method == 'POST':
        # Ajouter un utilisateur
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            is_admin = form.cleaned_data.get("is_admin")
            nieuw_wachtwoord = random_string(10)
            #TODO is de superuser hier goed gezet?
            new_user = User.objects.create_user(
                username=username,
                email=email,
                password=nieuw_wachtwoord,
                is_superuser=is_admin
            )
            new_user.save()
            #Hier het wachtwoord resettten
            
            
    else:
        form = UserCreationForm()
    return render(request, 'musicmix/usercreation.html', {"form": form})
    

def perform_auth_check(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        raise PermissionDenied()
    return True

def random_string(len: int) -> str:
    letters = "1234567890ABCDEFGHIJKLMNOP"
    result = ''
    for i in range(len):
        nummer = randint(0, len(letters) - 1)
        gekozen = letters[nummer]
        result = result + gekozen
    return result

