from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.utils.safestring import mark_safe
import os, random

# Create your models here.

class Awsaccounts(models.Model):
    accountName             = models.CharField(max_length=150, verbose_name='Account Name', blank=True)
    accountID               = models.CharField(max_length=50, verbose_name='Account ID', blank=True)
    accountUser             = models.CharField(max_length=150, verbose_name='Account User', blank=True)
    accessKeyID             = models.CharField(max_length=150, verbose_name='Access Key ID', blank=True)
    secretAccessKey         = models.CharField(max_length=150, verbose_name='Secret Access Key', blank=True)
    region                  = models.CharField(max_length=150, verbose_name='Region', blank=True)

class Aws(models.Model):
    accountName             = models.CharField(max_length=150, verbose_name='Account Name', blank=True)
    accountID               = models.CharField(max_length=50, verbose_name='Account ID', blank=True)
    accountUser             = models.CharField(max_length=150, verbose_name='Account User', blank=True)
    accessKeyID             = models.CharField(max_length=150, verbose_name='Access Key ID', blank=True)
    secretAccessKey         = models.CharField(max_length=150, verbose_name='Secret Access Key', blank=True)
    instanceName            = models.CharField(max_length=150, verbose_name='Instance Name', blank=True)
    instanceID              = models.CharField(max_length=150, verbose_name='Instance ID', blank=True)
    region                  = models.CharField(max_length=150, verbose_name='Region', blank=True)
    serverIP                = models.CharField(max_length=150, verbose_name='Server IP', blank=True)
    database                = models.CharField(max_length=150, verbose_name='Database', blank=True)
    serverType              = models.CharField(max_length=150, verbose_name='Server Type', blank=True)
    setupDate               = models.DateField(verbose_name='Setup Date', default=now)
    area                    = models.CharField(max_length=150, verbose_name='Area', blank=True)
    rdpPass                 = models.CharField(max_length=150, verbose_name='RDP Password', blank=True)


           