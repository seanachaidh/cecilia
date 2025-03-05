from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Label(models.Model):
    class LabelType(models.TextChoices):
        INSTRUMENT = 'INSTRUMENT', "Instrument"
        STEM = 'STEM', 'Stem'
        SLEUTEL = 'SLEUTEL', 'Sleutel'

    text = models.CharField(max_length=200)
    label_type = models.CharField(max_length=25, choices=LabelType.choices)

    @staticmethod
    def label_types():
        return Label.LabelType.choices

    def __str__(self) -> str:
        lower_type = self.label_type.lower().__str__()
        label_text = self.text.__str__()
        return f'{label_text} ({lower_type})'


class MusicPiece(models.Model):
    _youtube_format = 'https://www.youtube.com/watch?v={id}'

    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads')
    labels = models.ManyToManyField(Label)
    active = models.BooleanField(default=False)
    youtube_id = models.CharField(max_length=20, blank=True)

    def __str__(self) -> str:
        return self.title.__str__()

    def has_youtube(self):
        return self.youtube_id is not None and len(self.youtube_id.strip()) > 0

    def get_youtube_url(self):
        if self.has_youtube():
            return self._youtube_format.format(id=self.youtube_id)
        else:
            return None


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

    def collect_labels(self, t: Label.LabelType) -> list[int]:
        return list(self.labels.filter(label_type=t).values_list('id', flat=True))

class PasswordReset(models.Model):
    token = models.CharField(max_length=20)
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
