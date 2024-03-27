from django.db import models


# Create your models here.

class Label(models.Model):
    class LabelType(models.TextChoices):
        INSTRUMENT = 'INSTRUMENT', "Instrument"
        STEM = 'STEM', 'Stem'
        SLEUTEL = 'SLEUTEL', 'Sleutel'

    text = models.CharField(max_length=200)
    label_type = models.CharField(max_length=25, choices=LabelType.choices)

    def __str__(self) -> str:
        lower_type = self.label_type.lower().__str__()
        label_text = self.text.__str__()
        return f'{label_text} ({lower_type})'


class MusicPiece(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField()
    labels = models.ManyToManyField(Label)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title.__str__()
