from django import forms
from dao.labelrepo import fetch_all_choices_for_type


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.CharField(label="password", max_length=255, required=True)


class LabelRegistrationForm(forms.Form):

    def __init__(self):
        super().__init__()
        # Instruments
        choices = fetch_all_choices_for_type('INSTRUMENT')
        self.instruments = forms.ChoiceField(label='Instrument', choices=choices)

