from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.utils.safestring import mark_safe
import os, random

#now = timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    randomstr =''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'client_pic/{year}-{month}-{day}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance,
                                                                                        basename=basefilename,
                                                                                        randomstring=randomstr,
                                                                                        ext=file_extension,
                                                                                        year=_now.strftime('%Y'),
                                                                                        month=_now.strftime('%m'),
                                                                                        day=_now.strftime('%d'))

class Client(models.Model):
    client_fname        = models.CharField(max_length=200, verbose_name='First Name', blank=True)
    client_mname        = models.CharField(max_length=200, verbose_name='First Name', blank=True)
    client_lname        = models.CharField(max_length=200, verbose_name='Last Name', blank=True)
    client_email        = models.CharField(max_length=100, verbose_name='Email', blank=True)
    client_status       = models.CharField(max_length=200, verbose_name='Position', blank=True)
    client_gender       = models.CharField(max_length=50, verbose_name='Gender', blank=True)
    client_branch       = models.CharField(max_length=200, verbose_name='Client Branch', blank=True)
    client_children     = models.CharField(max_length=200, verbose_name='Children', blank=True)
    client_image        = models.ImageField(upload_to=image_path, default='client_pic/default_image.png')
    client_dob          = models.DateField(max_length=20, verbose_name='Client date of birth', default=now)
    client_cstatus      = models.CharField(max_length=50, verbose_name='Civil Status', blank=True)
    client_spouse       = models.CharField(max_length=50, verbose_name='Client Spouse', blank=True)
    client_address      = models.CharField(max_length=100, verbose_name='Client Address', blank=True)
    client_celnumber    = models.CharField(max_length=30, verbose_name='Client Cell Number', blank=True)
    client_membertype   = models.CharField(max_length=100, verbose_name='Members Type', blank=True)
    client_occupation   = models.CharField(max_length=100, verbose_name='Clients Occupation ', blank=True)
    client_cycle        = models.IntegerField(default=0, verbose_name='Clients Cycle')
    client_zipcode      = models.CharField(max_length=5, verbose_name='Zip Code', blank=True)
    client_branchcode   = models.CharField(max_length=5, verbose_name='Branch Code', blank=True)
    client_code         = models.CharField(max_length=20, verbose_name='Client Code', blank=True)
    client_isdisabled   = models.BooleanField(verbose_name='Is Disableden', default=False)


    def image_tag(self):
        return mark_safe('<img src="/clients/media/%s" width="50" height"50" />'%(self.client_image))
    reg_date = models.DateField(default=now)

    def __str__(self):
        return self.client_email

class Gender(models.Model):
    genders = models.CharField(max_length=20, verbose_name='Gender', blank=True)
    def __str__(self):
        return self.genders


class Civilstat(models.Model):
    civil_status = models.CharField(max_length=30, verbose_name='Civil Status', blank=True)
    def __str__(self):
        return self.civil_status


class Product(models.Model):
    products = models.CharField(max_length=50, verbose_name='Products', blank=True)
    def __str__(self):
        return self.products

class Membertype(models.Model):
    membertypes = models.CharField(max_length=50, verbose_name='Membership Type', blank=True)
    def __str__(self):
        return self.membertypes

class Clientstat(models.Model):
    client_status = models.CharField(max_length=50, verbose_name='Client Status', blank=True)
    def __str__(self):
        return self.client_status
    
class Branch(models.Model):
    branches = models.CharField(max_length=50, verbose_name='Branches', blank=True)
    def __str__(self):
        return self.branches

class Clientaccountcode(models.Model):
    branch            = models.CharField(max_length=20, verbose_name='Branch', blank=True)
    zipcode           = models.CharField(max_length=5, verbose_name='Zip Code', blank=True)
    branchcode        = models.CharField(max_length=5, verbose_name='Branch Code', blank=True)
    def __str__(self):
        return self.branch



