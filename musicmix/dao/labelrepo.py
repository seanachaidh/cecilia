from ..models import Label
from ..models import Profile


def fetch_all_labels():
    Label.objects.all()

def collect_labels():
    result = []
    choices = Label.label_types()
    for c, l in choices:
        labels = fetch_all_choices_for_type((c, l))
        result.append((c, l, labels))
    return result
def fetch_all_choices_for_type(label_type):
    result_list = []
    result = Label.objects.filter(label_type=label_type)
    for x in result:
        result_list.append((x.id, x.text))
    return result_list


def fetch_labels_for_profile(profile: Profile) -> list[Label]:
    return_value = Label.objects.filter(profile=profile)
    return return_value
def save_labels_for_profile(profile, labels):
    pass


def get_labels_from_ids(ids: list[int]) -> list[Label]:

    return list(map(lambda x: Label.objects.get(pk=x), ids))

