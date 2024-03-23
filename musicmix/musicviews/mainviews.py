from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

from musicmix.forms import LoginForm


# Create your views here.
def index(request):
    # If the user is not authenticated, the user must first log in
    if not request.user.is_authenticated:
        return redirect('/login')

    return render(request, template_name='musicmix/index.html')


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
                return redirect("/musicmix")
            else:
                messages.add_message(request, messages.ERROR, "Inloggen mislukt")

        return render(request, 'musicmix/login.html', {'form': form})

    else:
        form = LoginForm()
    return render(request, 'musicmix/login.html', {'form': form})
