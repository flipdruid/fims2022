# Generated by Django 3.2.3 on 2021-10-01 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0008_auto_20211001_0919'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='client_active',
        ),
    ]
