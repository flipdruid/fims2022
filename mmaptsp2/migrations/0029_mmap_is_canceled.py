# Generated by Django 4.0.5 on 2022-06-23 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmaptsp2', '0028_remove_mmap_is_canceled'),
    ]

    operations = [
        migrations.AddField(
            model_name='mmap',
            name='is_canceled',
            field=models.BooleanField(default=False, verbose_name='Is Canceled'),
        ),
    ]
