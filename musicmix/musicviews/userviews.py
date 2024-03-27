from django.views import View
from ..forms import LabelRegistrationForm
from django.shortcuts import render


class LabelRegistrationView(View):
    def get(self, request):
        form = LabelRegistrationForm()
        return render(request=request, template_name='musicmix/labelregistration.html', context={'form': form})

    def post(self, request):
        pass
