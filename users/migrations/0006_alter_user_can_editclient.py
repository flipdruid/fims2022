# Generated by Django 4.0.2 on 2022-02-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_can_editclient'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='can_editclient',
            field=models.BooleanField(default=True, verbose_name='Can edit client'),
        ),
    ]