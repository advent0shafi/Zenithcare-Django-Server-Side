# Generated by Django 4.2.5 on 2023-10-09 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0005_alter_therapist_certifications_delete_certification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='booking_schedule',
            field=models.ManyToManyField(blank=True, null=True, through='vendor.BookingSchedule', to='vendor.availableday'),
        ),
        migrations.RemoveField(
            model_name='therapist',
            name='languages',
        ),
        migrations.AddField(
            model_name='therapist',
            name='languages',
            field=models.ManyToManyField(to='vendor.language'),
        ),
    ]