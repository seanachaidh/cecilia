from django import forms
from .dao.labelrepo import fetch_all_choices_for_type
from .models import Label
from .widgets import ChipWidget


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.CharField(label="password", max_length=255, required=True)


class LabelRegistrationForm(forms.Form):

    def __init__(self, data=None):
        super(LabelRegistrationForm, self).__init__(data=data)
        choices_instruments = fetch_all_choices_for_type('INSTRUMENT')
        self.fields['instrument'] = forms.MultipleChoiceField(
            label='Instrumenten',
            widget=ChipWidget,
            choices=choices_instruments, required=False
        )

        choices_stem = fetch_all_choices_for_type('STEM')
        self.fields['stem'] = forms.MultipleChoiceField(
            label='Stem',
            widget=ChipWidget,
            choices=choices_stem, required=False
        )

    def populate(self, labels: list[Label]):
        label_types = dict()
        for label in labels:
            label_value = label_types.get(str(label.label_type), [])
            label_value.append(str(label.text))
            label_types[str(label.label_type)] = label_value
