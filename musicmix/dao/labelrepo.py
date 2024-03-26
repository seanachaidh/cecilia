from ..models import Label


def fetch_all_labels():
    Label.objects.all()


def fetch_all_choices_for_type(label_type):
    result_list = []
    result = Label.objects.filter(label_type=label_type)
    for x in result:
        result_list.append((x.id, x.text))
    return result_list
