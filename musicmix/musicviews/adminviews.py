from logging import info
from random import randint

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.uploadedfile import SimpleUploadedFile
from django.shortcuts import redirect, render, reverse
from django.views.decorators.http import require_POST
from django.views.generic import ListView

from .authutils import is_superuser
from ..forms import UserCreationForm, PieceCreationForm, UserUpdateForm
from ..models import *


@require_POST
@user_passes_test(is_superuser)
def remove_user(request, user_id):
    user = User.objects.get(pk=user_id)
    user.delete()
    return redirect(reverse('users'))

@require_POST
@user_passes_test(is_superuser)
def add_label(request, label_type):
    naam = request.POST.get("nieuwe")
    info('nieuw label met naam: ' + naam)
    
    #label maken
    label = Label()
    label.label_type = label_type
    label.text = naam
    label.save()
    
    return redirect(reverse('labels'))

@user_passes_test(is_superuser)
def remove_label(request, label_id):
    #Wat met mogelijke muziekstukken gekoppeld aan labels?
    label = Label.objects.get(pk=label_id)
    label.delete()
    return redirect(reverse('users'))

@user_passes_test(is_superuser)
def add_piece(request):
    if request.method == 'POST':
        form = PieceCreationForm(request.POST, request.FILES)
        if form.is_valid():
            save_piece(form)

            # Perfect bewaard. Terug naar admin
            return redirect(reverse('pieces'))
    else:
        #Wanneer het get is
        form = PieceCreationForm()
    return render(request, 'musicmix/basic_form.html', {"form": form, "is_file": True})


def save_piece(form):
    piece = MusicPiece()
    piece.active = True  # Maak hiervan nog een aanpasbare boolean
    piece.file = form.cleaned_data.get("file")
    piece.title = form.cleaned_data.get('title')
    piece.save()
    labels_instrument = form.cleaned_data.get('labels_instrument')
    labels_stem = form.cleaned_data.get('labels_stem')
    labels_sleutel = form.cleaned_data.get('labels_sleutel')
    full_list = labels_instrument + labels_sleutel + labels_stem
    fetched_labels = Label.objects.filter(pk__in=full_list)
    piece.labels.set(fetched_labels)
    piece.save()


@user_passes_test(is_superuser)
def delete_piece(request, piece_id):
    piece = MusicPiece.objects.get(pk=piece_id)
    piece.delete()
    return redirect(reverse('pieces'))

@user_passes_test(is_superuser)
def edit_piece(request, piece_id):
    piece = MusicPiece.objects.get(pk=piece_id)
    labels = piece.labels.values_list('id', 'label_type')
    labels_instrument = [x for x, y in labels if y == 'INSTRUMENT']
    labels_stem = [x for x, y in labels if y == 'STEM']
    labels_sleutel = [x for x, y in labels if y == 'SLEUTEL']

    if request.method == 'POST':
        form = PieceCreationForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            save_piece(form)
    else:
        title = piece.title
        file = piece.file
        file_content = file.read()
        data = {
            "title": title,
            "labels_instrument": labels_instrument,
            "labels_stem": labels_stem,
            "labels_sleutel": labels_sleutel,
            "file": file
        }
        files = {
            "file": SimpleUploadedFile(file.name, file_content)
        }
        form = PieceCreationForm(data=data, files=files)
    return render(request, 'musicmix/basic_form.html', {"form": form, "is_file": True})

@user_passes_test(is_superuser)
def add_user(request):
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
            return redirect(reverse('users'))
            
    else:
        form = UserCreationForm()
    return render(request, 'musicmix/basic_form.html', {"form": form})
    
def update_user(request, user_id):
    user = User.objects.get(pk=user_id)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            user.is_superuser = form.is_admin
            user.email = form.email
            user.save()
            return redirect(reverse('admin'))
    else:
        form = UserUpdateForm(
            is_admin=user.is_superuser,
            email=user.email
        )
    return render(request, 'musicmix/basic_form.html', {'form': form})


#TODO verander dit door een functie van django zelve
def random_string(length: int) -> str:
    letters = "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    result = ''
    for i in range(length):
        nummer = randint(0, len(letters) - 1)
        gekozen = letters[nummer]
        result = result + gekozen
    return result


class ProfilesListView(ListView, LoginRequiredMixin, UserPassesTestMixin):
    model = Profile
    context_object_name = 'profiles'
    template_name = 'musicmix/user_table.html'

    def test_func(self):
        return self.request.user.is_superuser


class PiecesListView(ListView):
    model = MusicPiece
    context_object_name = 'pieces'
