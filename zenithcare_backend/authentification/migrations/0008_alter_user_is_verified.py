# Generated by Django 4.2.5 on 2023-10-02 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0007_user_is_verified_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
