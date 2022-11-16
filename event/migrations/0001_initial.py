# Generated by Django 4.0.6 on 2022-07-14 11:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('can_pos', models.CharField(blank=True, max_length=50, verbose_name='Position')),
                ('can_branch', models.CharField(blank=True, max_length=50, verbose_name='Branch')),
                ('can_CBU', models.FloatField(blank=True, default=0, verbose_name='CBU')),
                ('can_savings', models.FloatField(blank=True, default=0, verbose_name='Savings')),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(blank=True, max_length=100, verbose_name='Event Name')),
                ('event_type', models.CharField(blank=True, max_length=50, verbose_name='Event Name')),
                ('event_date', models.DateTimeField(blank=True, verbose_name='Event Date')),
                ('event_setupDate', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Event Setup Date')),
            ],
        ),
        migrations.CreateModel(
            name='Event_positions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.CharField(blank=True, max_length=50, verbose_name='Position')),
                ('avail_seats', models.IntegerField(blank=True, default=0, verbose_name='Available Seats')),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voter_name', models.CharField(blank=True, max_length=100, verbose_name='Name')),
                ('voter_branch', models.CharField(blank=True, max_length=50, verbose_name='branch')),
                ('voter_CBU', models.FloatField(blank=True, default=0, verbose_name='CBU')),
                ('voter_savings', models.FloatField(blank=True, default=0, verbose_name='Savings')),
            ],
        ),
    ]