# Generated by Django 4.2.5 on 2023-10-12 04:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0006_alter_therapist_booking_schedule_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingschedule',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='bookingschedule',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='bookingschedule',
            name='time',
            field=models.CharField(blank=True, choices=[('10 AM', '10 AM'), ('10:20AM', '10:20AM'), ('11:40AM', '11:40 AM'), ('12:00 PM', '12:00 PM'), ('12:20 PM', '12:20 PM'), ('2:40 PM', '2:40 PM'), ('3 PM', '3 PM'), ('3:20 PM', '3:20 PM'), ('3:40 PM', '3:40 PM'), ('4:00 PM', '4:00 PM')], max_length=8, null=True),
        ),
        migrations.AlterField(
            model_name='bookingschedule',
            name='available_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='vendor.availableday'),
        ),
        migrations.AlterUniqueTogether(
            name='bookingschedule',
            unique_together={('therapist', 'date', 'time')},
        ),
        migrations.RemoveField(
            model_name='bookingschedule',
            name='available_hours_end',
        ),
        migrations.RemoveField(
            model_name='bookingschedule',
            name='available_hours_start',
        ),
    ]
