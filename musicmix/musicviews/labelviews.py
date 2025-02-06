from musicmix.dao.labelrepo import get_labels_from_ids
from musicmix.dao.profilerepo import find_or_create_profile
from musicmix.forms import LabelRegistrationForm


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View


class LabelData:

    def __init__(self, type, naam: str, geselecteerd: bool):
        self._type = type
        self._naam = naam
        self._geselecteerd = geselecteerd

    @property
    def type(self):
        return self._type
    @property
    def naam(self) -> str:
        return self._naam
    @property
    def geselecteerd(self) -> bool:
        return self._geselecteerd


class LabelRegistrationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        form = LabelRegistrationForm()
        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})

    def post(self, request):
        form = LabelRegistrationForm(request.POST)
        if form.is_valid():
            # These are all ID's of labels
            stem = form.cleaned_data.get('stem')
            instruments = form.cleaned_data.get('instrument')

            stem_objects = get_labels_from_ids(stem)
            instrument_objects = get_labels_from_ids(instruments)

            profile = find_or_create_profile(request.user)
            profile.labels.set(stem_objects + instrument_objects)
            profile.save()
            messages.add_message(request, messages.INFO, "Saving labels succeeded")
            return redirect("/musicmix")
        else:
            messages.add_message(request, messages.ERROR, "Request was invalid")
            render(request, template_name='musicmix/labelregistration.html', context={form: form})