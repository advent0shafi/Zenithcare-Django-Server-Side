# Generated by Django 4.2.5 on 2023-10-28 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0011_specilizations_therapist_specilizations'),
    ]

    operations = [
        migrations.AddField(
            model_name='therapist',
            name='degree1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='therapist',
            name='university',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
