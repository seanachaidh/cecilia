from logging import info
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail

from ..forms import PasswordResetInitForm
from ..mail import *
from ..models import PasswordReset
from ..dao.profilerepo import find_or_create_profile

def password_reset(request):
    if request.method == 'POST':
        form = PasswordResetInitForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['email']
            return password_reset_post(mail, request)
        else:
            return render(request, 'musicmix/basic_form.html', {'form': form})
    else:
        form = PasswordResetInitForm()
        return render(request, 'musicmix/basic_form.html', {'form': form})


def password_reset_post(email, request):
    info(f'Resetting password for {email}')
    # First we create a reset token
    random_token = get_random_string(length=20)
    user = get_object_or_404(User.objects.filter(email=email))
    profile = find_or_create_profile(user)
    password_reset_token = PasswordReset(token=random_token, user=profile)
    password_reset_token.save()
    # creating a absolute URI to the confirm view.
    template_url = reverse('password_reset_confirm', kwargs={'password_token': random_token})
    full_url = request.build_absolute_uri(template_url)
    # Creating the email
    contents = "Password reset initiated: go to {}".format(full_url)
    send_mail(
        'Password reset initiated',
        contents,
        'cecilia@seanachaidh.be',
        [email],
        fail_silently=False
    )
    return redirect(reverse('login'))


def password_reset_confirm(request, password_token: str):
    pass

