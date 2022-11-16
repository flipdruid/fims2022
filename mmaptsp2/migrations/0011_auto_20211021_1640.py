# Generated by Django 3.2.3 on 2021-10-21 16:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mmaptsp2', '0010_alter_sccn_mmap_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sccn',
            name='mmap_expired',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='MMAPExpriredDate'),
        ),
        migrations.AlterField(
            model_name='sccn',
            name='mmap_setupdate',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='MMAPSetupDate'),
        ),
    ]