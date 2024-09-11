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

class PieceCreationForm(forms.Form):
    title = forms.CharField(label="Titel", max_length=100)
    file = forms.FileField()
    
    def __init__(self, data=None):
        super(PieceCreationForm, self).__init__(data=data)
        labels = Label.objects.all()
        choices = [(x.) for x in labels]
        self.fields['labels'] = forms.MultipleChoiceField(
            Label="labels",
            widget=forms.CheckboxSelectMultiple,
            choices=
        )

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

    def populate(self, labels: list[Label]):
        label_types = dict()
        for label in labels:
            label_value = label_types.get(str(label.label_type), [])
            label_value.append(str(label.text))
            label_types[str(label.label_type)] = label_value
