from django import forms
from .dao.labelrepo import fetch_all_choices_for_type


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.CharField(label="password", max_length=255, required=True)


class LabelRegistrationForm(forms.Form):

    def __init__(self):
        super(LabelRegistrationForm, self).__init__()
        choices_instruments = fetch_all_choices_for_type('INSTRUMENT')
        self.fields['instruments'] = forms.MultipleChoiceField(
            label='Instrumenten',
            widget=forms.CheckboxSelectMultiple,
            choices=choices_instruments
        )

        choices_stem = fetch_all_choices_for_type('STEM')
        self.fields['parts'] = forms.MultipleChoiceField(
            label='Stem',
            widget=forms.CheckboxSelectMultiple,
            choices=choices_stem
        )

