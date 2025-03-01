from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from musicmix.forms import LabelRegistrationForm
from musicmix.models import Label, Profile


class LabelRegistrationView(LoginRequiredMixin, View):
    login_url = 'login'

    #TODO maak hier functies van
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        data = {
            'sleutel': profile.collect_labels(Label.LabelType.SLEUTEL),
            'stem': profile.collect_labels(Label.LabelType.STEM),
            'instrument': profile.collect_labels(Label.LabelType.INSTRUMENT)
        }
        form = LabelRegistrationForm(initial=data)
        
        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})

    def post(self, request):
        form = LabelRegistrationForm(request.POST)
        if form.is_valid():
            sleutel = form.cleaned_data.get('sleutel')
            stem = form.cleaned_data.get('stem')
            instrument = form.cleaned_data.get('instrument')

            # Ik denk dat ik deze gewoon kan samenvoegen?
            alle_labels = sleutel + stem + instrument
            profile = Profile.objects.get(user=request.user)
            profile.labels.clear()
            for label_id in alle_labels:
                # Haal de label op
                label = Label.objects.get(id=label_id)
                profile.labels.add(label)
            profile.save()

        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})
