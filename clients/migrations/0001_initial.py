# Generated by Django 3.2.3 on 2021-09-30 13:48

import clients.models
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branches', models.CharField(blank=True, max_length=50, verbose_name='Branches')),
            ],
        ),
        migrations.CreateModel(
            name='Civilstat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('civil_status', models.CharField(blank=True, max_length=30, verbose_name='Civil Status')),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_fname', models.CharField(blank=True, max_length=200, verbose_name='First Name')),
                ('client_mname', models.CharField(blank=True, max_length=200, verbose_name='First Name')),
                ('client_lname', models.CharField(blank=True, max_length=200, verbose_name='Last Name')),
                ('client_email', models.CharField(blank=True, max_length=100, verbose_name='Email')),
                ('client_status', models.CharField(blank=True, max_length=200, verbose_name='Position')),
                ('client_gender', models.CharField(blank=True, max_length=50, verbose_name='Gender')),
                ('client_branch', models.CharField(blank=True, max_length=200, verbose_name='Client Branch')),
                ('client_children', models.CharField(blank=True, max_length=200, verbose_name='Children')),
                ('client_image', models.ImageField(default='client_pic/default_image.jpg', upload_to=clients.models.image_path)),
                ('client_dob', models.DateField(default=django.utils.timezone.now, max_length=20, verbose_name='Client date of birth')),
                ('client_cstatus', models.CharField(blank=True, max_length=50, verbose_name='Civil Status')),
                ('client_spouse', models.CharField(blank=True, max_length=50, verbose_name='Client Spouse')),
                ('client_address', models.CharField(blank=True, max_length=100, verbose_name='Client Address')),
                ('client_celnumber', models.CharField(blank=True, max_length=30, verbose_name='Client Cell Number')),
                ('client_membertype', models.CharField(blank=True, max_length=100, verbose_name='Members Type')),
                ('client_occupation', models.CharField(blank=True, max_length=100, verbose_name='Clients Occupation ')),
                ('client_cycle', models.IntegerField(default=0, verbose_name='Clients Cycle')),
                ('client_active', models.BooleanField(default=False, verbose_name='is active')),
                ('reg_date', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Clientaccountcode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('branch', models.CharField(blank=True, max_length=20, verbose_name='Branch')),
                ('clientaccountcode', models.CharField(blank=True, max_length=3, verbose_name='Client Account Number')),
                ('Branchcode', models.CharField(blank=True, max_length=5, verbose_name='Branch Code')),
            ],
        ),
        migrations.CreateModel(
            name='Clientstat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_status', models.CharField(blank=True, max_length=50, verbose_name='Client Status')),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genders', models.CharField(blank=True, max_length=20, verbose_name='Gender')),
            ],
        ),
        migrations.CreateModel(
            name='Membertype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membertypes', models.CharField(blank=True, max_length=50, verbose_name='Membership Type')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.CharField(blank=True, max_length=50, verbose_name='Products')),
            ],
        ),
    ]