# Generated by Django 4.2.5 on 2023-10-09 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_remove_therapist_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='address',
            name='longitude',
        ),
    ]
