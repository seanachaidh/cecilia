from django.views import View
from ..forms import LabelRegistrationForm
from django.shortcuts import render
from django.contrib.auth.models import User
from ..dao.profilerepo import find_or_create_profile
from ..dao.labelrepo import fetch_labels_for_profile


# This function is way too long and can probably be written shorter
def populate_form(user: User):
    data = dict()
    profile = find_or_create_profile(user)
    labels = fetch_labels_for_profile(profile)
    for label in labels:
        key = str(label.label_type)
        value = str(label.text)

        label_value_list = data.get(key, [])
        label_value_list.append(value)
        data[key] = label_value_list

    return data


class LabelRegistrationView(View):

    def get(self, request):
        d = populate_form(request.user)
        form = LabelRegistrationForm(data=d)
        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})

    def post(self, request):
        pass

