# Generated by Django 3.2.3 on 2021-10-21 16:11

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mmaptsp2', '0009_auto_20211021_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sccn',
            name='mmap_expired',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='MMAP Exprired Date'),
        ),
    ]
