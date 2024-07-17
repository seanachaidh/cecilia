from django.shortcuts import redirect, render, reverse
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import user_passes_test
from authutils import is_superuser

from ..forms import UserCreationForm
from ..models import *
from random import randint

# TODO maak hier een paged list view van
@user_passes_test(is_superuser)
def show_admin_panel(request):
    check = perform_auth_check(request)
    if not check:
        return check
    users = User.objects.all()
    admin_context = {
        "users": users
    }
    return render(request=request, template_name='musicmix/adminpanel.html', context=admin_context)
    
@require_POST
@user_passes_test(is_superuser)
def remove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect(reverse('admin'))


@user_passes_test(is_superuser)
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
            #Hier het wachtwoord resetten
            return redirect(reverse('admin'))
            
    else:
        form = UserCreationForm()
    return render(request, 'musicmix/basic_form.html', {"form": form})
    

def perform_auth_check(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        raise PermissionDenied()
    return True
#TODO verander dit door een functie van django zelve
def random_string(length: int) -> str:
    letters = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ''
    for i in range(length):
        nummer = randint(0, len(letters) - 1)
        gekozen = letters[nummer]
        result = result + gekozen
    return result

