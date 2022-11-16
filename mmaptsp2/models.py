from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.utils.safestring import mark_safe
import os, random
from clients.models import Client 

#nowtoday=timezone.now()

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    randomstr =''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'mmaptsp2_pic/{year}-{month}-{day}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance,
                                                                                        basename=basefilename,
                                                                                        randomstring=randomstr,
                                                                                        ext=file_extension,
                                                                                        year=_now.strftime('%Y'),
                                                                                        month=_now.strftime('%m'),
                                                                                        day=_now.strftime('%d'))

class Mmap(models.Model):
    clientid                    = models.IntegerField(default=0, verbose_name='ClientID', blank=True)
    mmap_name                   = models.CharField(max_length=150, verbose_name='Name', blank=True)
    mmap_sex                    = models.CharField(max_length=20, verbose_name='Sex', blank=True)
    mmap_age                    = models.IntegerField(default=0, verbose_name='Age', blank=True)
    mmap_type                   = models.CharField(max_length=50, verbose_name='Type', blank=True)
    mmap_branch                 = models.CharField(max_length=50, verbose_name='Branch', blank=True)
    mmap_address                = models.CharField(max_length=200, verbose_name='Address', blank=True)
    mmap_setupdate              = models.DateField(verbose_name='MMAP Setup Date', default=now)
    recuited_by                 = models.CharField(max_length=50, verbose_name='Recruited by', blank=True)
    client_cycle                = models.IntegerField(default=0, verbose_name='Clients Cycle ', blank=True)
    mmap_dob                    = models.DateField(verbose_name='Date of Birth', default=now, blank=True)    
    processed_by                = models.CharField(max_length=50, verbose_name='Processed by', blank=True)
    processed_des               = models.CharField(max_length=50, verbose_name='Processed by', blank=True)
    processed_date              = models.DateField(verbose_name='Processed Date', default=now)
    checked_by                  = models.CharField(max_length=50, verbose_name='Checked by', blank=True)
    checked_des                 = models.CharField(max_length=50, verbose_name='Checked by', blank=True)
    checked_date                = models.DateField(verbose_name='Checked Date', default=now)
    approved_by                 = models.CharField(max_length=50, verbose_name='Approved by', blank=True)
    approved_des                = models.CharField(max_length=50, verbose_name='Approved by', blank=True)
    approved_date               = models.DateField(verbose_name='Approved Date', default=now)
    mmap_encodedate             = models.DateField(verbose_name='MMAP Date Encoded', default=now)
    mmap_expired                = models.DateField(verbose_name='MMAP Exprired Date', default=now)
    mmap_premium                = models.IntegerField(default=900, verbose_name='MMAP Premium')
    clientimg                   = models.ImageField(default='client_pic/default_image.jpg')
    mmapservicecentercontrolno  = models.CharField(max_length=10, default="None", verbose_name='MMAP Service Center Control Number', blank=False)
    mmapbcode                   = models.CharField(max_length=3, default="None", verbose_name='MMAP Branch Code', blank=True)
    client_code                 = models.CharField(max_length=15, default="None", verbose_name='MMAP Client Code', blank=True)
    expired_status              = models.BooleanField(verbose_name='MMAP Exprired Status', default=False)
    mmap_form_fimage            = models.ImageField(upload_to=image_path, default='mmaptsp2_pic/default_image.png', verbose_name='MMAP Front Form')
    mmap_form_bimage            = models.ImageField(upload_to=image_path, default='mmaptsp2_pic/default_image.png', verbose_name='MMAP Back Form')
    is_canceled                 = models.BooleanField(verbose_name='Is Canceled', default=False)
    def image_tagfront(self):
        return mark_safe('<img src="/mmaptsp2/media/%s" width="50" height"50" />'%(self.mmap_form_fimage))
    def image_tagback(self):
        return mark_safe('<img src="/mmaptsp2/media/%s" width="50" height"50" />'%(self.mmap_form_bimage))
    
    def __str__(self):
        return self.mmap_name   

class Beneficiary(models.Model):

    mmapid                          = models.CharField(max_length=10, default="None", verbose_name='MMAPID', blank=False)
    mmapservicecentercontrolno      = models.CharField(max_length=10, default="None", verbose_name='MMAP Service Center Control Number', blank=False)
    ben_mmap_name                   = models.CharField(max_length=150, verbose_name='Name', blank=True)
    mmap_clientid                   = models.IntegerField(default=0, verbose_name='mmap_clientid', blank=True)
    client_cycle                    = models.IntegerField(default=0, verbose_name='Clients Cycle ', blank=True)
    ben1                            = models.CharField(max_length=80, verbose_name='Beneficiary 1', blank=True, null=True) 
    ben2                            = models.CharField(max_length=80, verbose_name='Beneficiary 2', blank=True) 
    ben3                            = models.CharField(max_length=80, verbose_name='Beneficiary 3', blank=True) 

    ben1_dob                        = models.DateField(verbose_name='Beneficiary 1 DOB', default=now, blank=True, null=True)
    ben2_dob                        = models.DateField(verbose_name='Beneficiary 2 DOB', default=now, blank=True, null=True)
    ben3_dob                        = models.DateField(verbose_name='Beneficiary 3 DOB', default=now, blank=True, null=True)

    ben1_rel                        = models.CharField(max_length=80, verbose_name='Beneficiary 1 Relationship', blank=True, null=True) 
    ben2_rel                        = models.CharField(max_length=80, verbose_name='Beneficiary 2 Relationship', blank=True, null=True) 
    ben3_rel                        = models.CharField(max_length=80, verbose_name='Beneficiary 3 Relationship', blank=True, null=True)


class Sccn(models.Model): 
    mmap_encodedate             = models.DateTimeField(verbose_name='MMAP Date Encoded', default=now)
    sscnservicecentercontrolno  = models.CharField(max_length=10, verbose_name='Service Center Control Number', blank=True)
    client_name                 = models.CharField(max_length=150, verbose_name='Client Name', blank=True)
    sccnbcode                   = models.CharField(max_length=10, default="None", verbose_name='Branch Code', blank=True)
    sccnbranch                  = models.CharField(max_length=15, default="None", verbose_name='SCCN Branch', blank=True)
    mmap_setupdate              = models.DateField(verbose_name='MMAPSetupDate', default=now)
    mmap_expired                = models.DateField(verbose_name='MMAPExpriredDate', default=now)

class Branchcode(models.Model): 
    bcode           = models.CharField(max_length=3, default="", verbose_name='BranchCode', blank=True)
    bname           = models.CharField(max_length=150, verbose_name='BranchName', blank=True)
    dateadded       = models.DateTimeField(verbose_name='Date added', default=now, blank=True, null=True)