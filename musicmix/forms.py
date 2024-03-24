from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="username", max_length=20, required=True)
    password = forms.CharField(label="password", max_length=255, required=True)


class LabelRegistrationForm(forms.Form):

    def __init__(self):
        super().__init__()

