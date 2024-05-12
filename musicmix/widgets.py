from django.forms.widgets import Widget, RadioSelect

class ChipWidget(RadioSelect):
    class Media:
        css = {
            "all": ["/css/chips.css"]
        }
    allow_multiple_selected = True
    option_template_name = 'musicmix/widgets/chip.html'
    template_name = 'musicmix/widgets/chip-container.html'
    
    
    