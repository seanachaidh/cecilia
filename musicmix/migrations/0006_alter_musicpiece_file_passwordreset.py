# Generated by Django 4.2.11 on 2024-06-29 12:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('musicmix', '0005_remove_profile_labels_profile_labels'),
    ]

    operations = [
        migrations.AlterField(
            model_name='musicpiece',
            name='file',
            field=models.FileField(upload_to='uploads'),
        ),
        migrations.CreateModel(
            name='PasswordReset',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='musicmix.profile')),
            ],
        ),
    ]
