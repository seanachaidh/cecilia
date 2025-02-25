from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from .. import logger

from musicmix.models import Label, Profile
from musicmix.forms import LabelRegistrationForm

class LabelTypeData:

    def __init__(self, label_type):
        self._type = label_type
        self._labels: list[LabelData] = []

    @property
    def label_type(self):
        return self._type
    
    @property
    def labels(self):
        return self._labels
    
    def add(self, data):
        self._labels.append(data)
    
    @staticmethod
    def with_list(label_type: Label.LabelType, data_list: list[Label]):
        return_value = LabelTypeData(label_type)
        for d in data_list:
            return_value.add(LabelData(d.id, d.text, False))
        return return_value

class LabelData:

    def __init__(self, label_id: int, naam: str, geselecteerd: bool):
        self._naam = naam
        self._geselecteerd = geselecteerd
        self._id = label_id

    @property
    def naam(self) -> str:
        return self._naam
    @property
    def label_id(self) -> int:
        return self._id
    @property
    def geselecteerd(self) -> bool:
        return self._geselecteerd

    @geselecteerd.setter
    def geselecteerd(self, new_geselecteerd: bool):
        self._geselecteerd = new_geselecteerd


class LabelRegistrationView(LoginRequiredMixin, View):
    login_url = 'login'

    #TODO maak hier functies van
    def get(self, request):
        user = request.user
        
        form = LabelRegistrationForm()

        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})

    def post(self, request):
        # TODO ik moet dit refactoren zodat het gebruik maakt van het Form systeem van django.
        form = LabelRegistrationForm(request.POST)
        if form.is_valid():
            sleutel = form.cleaned_data.get('sleutel')
            logger.info("sleutel labels: %s", sleutel)
        return HttpResponse('')
            


# few utility functions to handle labels
def collect_labels(user: Profile, label_type: Label.LabelType) -> LabelTypeData:
    # TODO kan dit in één keer?
    profile = Profile.objects.filter(user=user).get()
    labels = profile.labels.filter(label_type=label_type)
    return LabelTypeData.with_list(label_type, list(labels))

def collect_all_labels(label_type):
    labels = Label.objects.filter(label_type=label_type)
    return LabelTypeData.with_list(label_type, list(labels))

def select_labels(user_labels: LabelTypeData, all_labels: LabelTypeData):
    for l in all_labels.labels:
        l.geselecteerd = any(x.label_id == l.label_id for x in user_labels.labels)

def filter_keys(labels: dict[str, str], label_type: Label.LabelType) -> dict[str, str]:
    return {k: v for k, v in labels.items() if k.endswith(str(label_type))}

def edit_labels(new_labels: dict[str, str], profile: Profile):
    profile.labels.clear()
    for k, v in new_labels.items():
        # fetch label
        if v:
            label_name, label_type = k.split('|')
            label = Label.objects.get(label_type=label_type, text=label_name)
            profile.labels.add(label)
    profile.save()