# Generated by Django 4.2.5 on 2023-10-23 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_payment_vendor_user_alter_payment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='isPaid',
            field=models.BooleanField(default=True),
        ),
    ]
