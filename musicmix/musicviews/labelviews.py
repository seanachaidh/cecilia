from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from musicmix.forms import LabelRegistrationForm
from musicmix.models import Label, Profile


def labels_post(request):
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
        messages.success(request, 'Labels zijn opgeslagen.')

    return render(request=request, template_name='musicmix/label-registration.html', context={'form': form})


def labels_get(request):
    profile = Profile.objects.get(user=request.user)
    data = {
        'sleutel': profile.collect_labels(Label.LabelType.SLEUTEL),
        'stem': profile.collect_labels(Label.LabelType.STEM),
        'instrument': profile.collect_labels(Label.LabelType.INSTRUMENT)
    }
    form = LabelRegistrationForm(initial=data)

    return render(request=request, template_name='musicmix/label-registration.html', context={'form': form})


@login_required(login_url='login')
def handle_labels(request):
    if request.method == 'POST':
        return labels_post(request)
    else:
        return labels_get(request)