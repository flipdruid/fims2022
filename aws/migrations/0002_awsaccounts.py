# Generated by Django 4.0.5 on 2022-06-16 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aws', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Awsaccounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accountName', models.CharField(blank=True, max_length=150, verbose_name='Account Name')),
                ('accountID', models.IntegerField(blank=True, default=0, verbose_name='Account ID')),
                ('accountUser', models.CharField(blank=True, max_length=150, verbose_name='Account User')),
                ('accessKeyID', models.CharField(blank=True, max_length=150, verbose_name='Access Key ID')),
                ('secretAccessKey', models.CharField(blank=True, max_length=150, verbose_name='Secret Access Key')),
                ('instanceName', models.CharField(blank=True, max_length=150, verbose_name='Instance Name')),
                ('region', models.CharField(blank=True, max_length=150, verbose_name='Region')),
            ],
        ),
    ]