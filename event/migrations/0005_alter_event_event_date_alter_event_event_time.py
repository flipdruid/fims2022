# Generated by Django 4.0.6 on 2022-07-17 23:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0004_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(blank=True, default='23:22:19', verbose_name='Event Date'),
        ),
    ]
