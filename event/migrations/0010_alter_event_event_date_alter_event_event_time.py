# Generated by Django 4.0.6 on 2022-07-26 15:03

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_event_user_id_event_user_name_alter_event_event_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Event Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='event_time',
            field=models.TimeField(default='15:03', verbose_name='Event Time'),
        ),
    ]
