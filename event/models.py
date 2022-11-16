from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now

# Create your models here.
time_now = datetime.now().strftime('%H:%M')   


class Event(models.Model):
    event_name          =   models.CharField(max_length=100, verbose_name='Event Name', blank=True)
    event_type          =   models.CharField(max_length=50, verbose_name='Event Type', blank=True)
    event_date          =   models.DateField(verbose_name='Event Date',  default=now)    
    event_time          =   models.TimeField(verbose_name='Event Time',  default = time_now)
    event_setupDate     =   models.DateField(verbose_name='Event Setup Date', default=now)
    user_id             =   models.IntegerField(default=0, verbose_name='User ID', blank=True)
    user_name           =   models.CharField(max_length=50, verbose_name='User Name', blank=True)


class Event_type(models.Model):
    event_type_name     =   models.CharField(max_length=100, verbose_name='Event Type Name', blank=True)
    event_description   =   models.TextField(max_length=150, verbose_name='Event Description', blank=True)

class Event_positions(models.Model):
    eventid             =   models.IntegerField(default=0, verbose_name = "Event ID")
    position            =   models.CharField(max_length=50, verbose_name='Position', blank=True)
    avail_seats         =   models.IntegerField(default=0, verbose_name='Available Seats', blank=True)

class Candidates(models.Model):
    eventid             =   models.IntegerField(default=0, verbose_name = "Event ID")
    can_name            =   models.CharField(max_length=100, verbose_name='Name', blank=True)
    can_pos             =   models.CharField(max_length=50, verbose_name='Position', blank=True)
    can_branch          =   models.CharField(max_length=50, verbose_name= 'Branch', blank=True)
    can_CBU             =   models.FloatField(default=0, verbose_name='CBU', blank=True)
    can_savings         =   models.FloatField(default=0, verbose_name='Savings', blank=True)
    position            =   models.CharField(max_length=50, verbose_name='Position', blank=True)

class Voter(models.Model):
    eventid             =   models.IntegerField(default=0, verbose_name = "Event ID")
    voter_name          =   models.CharField(max_length=100, verbose_name='Name', blank=True)
    voter_branch        =   models.CharField(max_length=50, verbose_name='branch', blank=True)
    voter_CBU           =   models.FloatField(default=0, verbose_name='CBU', blank=True)
    voter_savings       =   models.FloatField(default=0, verbose_name='Savings', blank=True)
    # voter_regdate       =   models.DateTimeField(verbose_name='Registered Date',  default=now) 

class Key_var(models.Model):
    eventid             =   models.IntegerField(default=0, verbose_name = "Event ID")
    eventcaption        =   models.CharField(max_length=50, verbose_name='Event Caption', blank=True)


    