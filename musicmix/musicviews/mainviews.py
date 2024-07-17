from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from musicmix.forms import LoginForm

@login_required(login_url='login')
def index(request):
    return render(request, template_name='musicmix/index.html')

@login_required(login_url='login')
def logout_user(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect(reverse('login'))


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Back to main screen
                return redirect("../musicmix")
            else:
                messages.add_message(request, messages.ERROR, "Inloggen mislukt")

        return render(request, 'musicmix/login.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'musicmix/login.html', {'form': form})
