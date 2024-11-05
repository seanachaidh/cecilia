from django import forms
from .dao.labelrepo import fetch_all_choices_for_type
from .models import Label
from django.forms.widgets import PasswordInput

class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.CharField(label="password", max_length=255, required=True, widget=PasswordInput)
    
class PasswordResetForm(forms.Form):
    new_password = forms.CharField(label="Nieuw wachtwoord", widget=PasswordInput)
    retype_new_password = forms.CharField(label="Nieuw wachtwoord hertypen", widget=PasswordInput)
    password_token = forms.HiddenInput()

    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        value1 = cleaned_data.get('new_password')
        value2 = cleaned_data.get('retype_new_password')

        #TODO Show validation errors in form
        if value1 != value2:
            raise forms.ValidationError("De wachtwoorden moeten gelijk zijn")
        return cleaned_data


class PasswordResetInitForm(forms.Form):
    email = forms.EmailField(label="Email", required=True, widget=forms.EmailInput)

class UserCreationForm(forms.Form):
    username = forms.CharField(label="Gebruikersnaam", max_length=20, required=True)
    email = forms.EmailField(label="E-mail", required=True)
    is_admin = forms.BooleanField(label="Is administrator", required=False)

class UserUpdateForm(forms.Form):
    email = forms.EmailField(label="E-mail", required=True)
    is_admin = forms.BooleanField(label="Is administrator", required=False)

    
class PieceEditForm(forms.Form):
    title = forms.CharField(label="Titel", max_length=100)
    
    def __init__(self, data=None, files=None):
        super(PieceEditForm, self).__init__(data=data, files=files)
        choices_instrument = self._fetch_labels('INSTRUMENT')
        choices_stem = self._fetch_labels('STEM')
        choices_sleutel = self._fetch_labels('SLEUTEL')
        self.fields['labels_stem'] = forms.MultipleChoiceField(
            label="Stem",
            widget=forms.CheckboxSelectMultiple,
            choices=choices_stem,
            required=False
        )
        self.fields['labels_instrument'] = forms.MultipleChoiceField(
            label="Instrumenten",
            widget=forms.CheckboxSelectMultiple,
            choices=choices_instrument,
            required=False
        )
        self.fields['labels_sleutel'] = forms.MultipleChoiceField(
            label="Sleutel",
            widget=forms.widgets.CheckboxSelectMultiple,
            choices=choices_sleutel,
            required=False
        )
        
    def _fetch_labels(self, label_type: str) -> list[tuple]:
        l = Label.objects.filter(label_type=label_type)
        return [(x.id, x.text) for x in l]

class PieceCreationForm(PieceEditForm):
    file = forms.FileField(label="Bestand")

class LabelRegistrationForm(forms.Form):

    def __init__(self, data=None):
        super(LabelRegistrationForm, self).__init__(data=data)
        choices_instruments = fetch_all_choices_for_type('INSTRUMENT')
        self.fields['instrument'] = forms.MultipleChoiceField(
            label='Instrumenten',
            widget=forms.CheckboxSelectMultiple,
            choices=choices_instruments, required=False
        )

        choices_stem = fetch_all_choices_for_type('STEM')
        self.fields['stem'] = forms.MultipleChoiceField(
            label='Stem',
            widget=forms.CheckboxSelectMultiple,
            choices=choices_stem, required=False
        )

        choice_key = fetch_all_choices_for_type('SLEUTEL')
        self.fields['sleutel'] = forms.MultipleChoiceField(
            label='Sleutel',
            widget=forms.CheckboxSelectMultiple,
            choices=choice_key, required=False
        )

    def populate(self, labels: list[Label]):
        label_types = dict()
        for label in labels:
            label_value = label_types.get(str(label.label_type), [])
            label_value.append(str(label.text))
            label_types[str(label.label_type)] = label_value
