# Generated by Django 4.2.11 on 2024-04-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicmix', '0004_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='labels',
        ),
        migrations.AddField(
            model_name='profile',
            name='labels',
            field=models.ManyToManyField(to='musicmix.label'),
        ),
    ]
