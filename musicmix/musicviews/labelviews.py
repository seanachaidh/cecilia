from musicmix.dao.labelrepo import get_labels_from_ids
from musicmix.dao.profilerepo import find_or_create_profile
from musicmix.forms import LabelRegistrationForm
from musicmix.models import Label, Profile


from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View

class LabelTypeData:

    def __init__(self, type):
        self._type = type
        self._labels: list[LabelData] = []

    @property
    def type(self):
        return self._type
    
    @property
    def labels(self):
        return self._labels
    
    def add(self, data):
        self._labels.append(data)
    
    @staticmethod
    def with_list(type, data_list):
        return_value = LabelTypeData(type)
        for d in data_list:
            return_value.add(d)
        return return_value

class LabelData:

    def __init__(self, naam: str, geselecteerd: bool):
        self._naam = naam
        self._geselecteerd = geselecteerd

    @property
    def naam(self) -> str:
        return self._naam
    @property
    def geselecteerd(self) -> bool:
        return self._geselecteerd


class LabelRegistrationView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        labels_sleutel = collect_labels(user, Label.LabelType.SLEUTEL)
        labels_sleutel_all = collect_all_labels(Label.LabelType.SLEUTEL)
        select_labels(labels_sleutel, labels_sleutel_all)
        
        
        return render(request=request, template_name='musicmix/labelregistration.html', context={'labels_sleutel': labels_sleutel_all})

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
            
            
# few utitlity functions to handle labels
def collect_labels(user, label_type) -> LabelTypeData:
    # TODO kan dit in één keer?
    profile = Profile.objects.filter(user=user).get()
    labels = profile.labels.filter(label_type=label_type)
    return LabelTypeData.with_list(label_type, list(labels))

def collect_all_labels(label_type):
    labels = Label.objects.filter(label_type=label_type)
    return LabelTypeData.with_list(label_type, list(labels))

def select_labels(user_labels, all_labels: LabelTypeData):
    for l in all_labels.labels:
        l.geselecteerd = any(x.id == l.id for x in user_labels.labels)