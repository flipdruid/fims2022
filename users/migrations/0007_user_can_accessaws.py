# Generated by Django 4.0.5 on 2022-06-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_can_editclient'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_accessaws',
            field=models.BooleanField(default=False),
        ),
    ]
