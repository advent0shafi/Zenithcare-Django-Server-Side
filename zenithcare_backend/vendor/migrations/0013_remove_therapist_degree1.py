# Generated by Django 4.2.5 on 2023-10-28 03:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0012_therapist_degree1_therapist_university'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='therapist',
            name='degree1',
        ),
    ]
