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

    def __str__(self) -> str:
        lower_type = self.label_type.lower().__str__()
        label_text = self.text.__str__()
        return f'{label_text} ({lower_type})'


class MusicPiece(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads')
    labels = models.ManyToManyField(Label)
    active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title.__str__()


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    labels = models.ManyToManyField(Label)

class PasswordReset(models.Model):
    token = models.CharField(max_length=20)
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING)
