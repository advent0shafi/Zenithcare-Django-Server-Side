# Generated by Django 4.2.5 on 2023-10-16 05:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vendor', '0008_remove_therapist_booking_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionMode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('booking_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_of_booking', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('cancel', 'Cancelled')], default='pending', max_length=10)),
                ('payment_type', models.CharField(choices=[('online', 'Online Payment'), ('wallet', 'Wallet')], default='online', max_length=10)),
                ('token', models.CharField(editable=False, max_length=6, unique=True)),
                ('mode_of_session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor_booking.sessionmode')),
                ('slot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.bookingschedule')),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vendor.therapist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]