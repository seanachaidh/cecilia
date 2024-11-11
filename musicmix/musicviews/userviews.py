from logging import info

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from ..dao.labelrepo import fetch_labels_for_profile, get_labels_from_ids
from ..dao.profilerepo import find_or_create_profile
from ..forms import LabelRegistrationForm
from ..models import MusicPiece, Profile


# This function is way too long and can probably be written shorter
# @login_required(login_url='login')
def populate_form(user: User):
    data = dict()
    profile = find_or_create_profile(user)
    labels = fetch_labels_for_profile(profile)
    for label in labels:
        key = str(label.label_type.lower())
        value = str(label.pk)

        label_value_list = data.get(key, [])
        label_value_list.append(value)
        data[key] = label_value_list

    return data

class OverviewView(LoginRequiredMixin, ListView):
    model = MusicPiece
    paginate_by = 5
    ordering = ['title']
    template_name = "musicmix/musicpieceoverview.html"
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
class MyPiecesView(LoginRequiredMixin, ListView):
    paginate_by = 5
    ordering = ['title']
    template_name = "musicmix/musicpieceoverview.html"
    login_url = 'login'

    def get_queryset(self):
        current_user = self.request.user
        profile = find_or_create_profile(current_user)
        return self._fetch_current_pieces(profile)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def _fetch_current_pieces(self, profile: Profile):
        labels = profile.labels.all()
        return MusicPiece.objects.filter(active=True, labels__in=labels)

class LabelRegistrationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        d = populate_form(request.user)
        form = LabelRegistrationForm(data=d)
        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})

    def post(self, request):
        form = LabelRegistrationForm(request.POST)
        if form.is_valid():
            # These are all ID's of labels
            stem = form.cleaned_data.get('stem')
            instruments = form.cleaned_data.get('instrument')

            stem_objects = get_labels_from_ids(stem)
            instrument_objects = get_labels_from_ids(instruments)

            info("saving labels")
            profile = find_or_create_profile(request.user)
            profile.labels.set(stem_objects + instrument_objects)
            profile.save()
            messages.add_message(request, messages.INFO, "Saving labels succeeded")
            return redirect("/musicmix")
        else:
            messages.add_message(request, messages.ERROR, "Request was invalid")
            render(request, template_name='musicmix/labelregistration.html', context={form: form})
