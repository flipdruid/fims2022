# Generated by Django 4.0.4 on 2022-04-13 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mmaptsp2', '0016_rename_recruited_by_mmap_recuited_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='mmapid',
            field=models.CharField(default='None', max_length=10, verbose_name='MMAP ID'),
        ),
    ]
