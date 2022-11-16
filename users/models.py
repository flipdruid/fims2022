from django.db import models
from datetime import datetime
from django.utils import timezone
from django.utils.timezone import now
from django.utils.safestring import mark_safe
import os, random

#
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

#now = timezone.now()
#_now = now

def image_path(instance, filename):
    basefilename, file_extension = os.path.splitext(filename)
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    randomstr =''.join((random.choice(chars)) for x in range(10))
    _now = datetime.now()

    return 'profile_pic/{year}-{month}-{day}-{imageid}-{basename}-{randomstring}{ext}'.format(imageid = instance,
                                                                                        basename=basefilename,
                                                                                        randomstring=randomstr,
                                                                                        ext=file_extension,
                                                                                        year=_now.strftime('%Y'),
                                                                                        month=_now.strftime('%m'),
                                                                                        day=_now.strftime('%d'))



class CustomAccountManager(BaseUserManager):

    def create_superuser(self, user_email, user_name, user_fname, user_lname, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError ('Superuser must be assigned to is_staff=True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError ('Superuser must be assigned to is_superuser=True')        
        return self.create_user(user_email, user_name, user_fname, user_lname, password, **other_fields)


    def create_user(self, user_email, user_name, user_fname, user_lname, password, **other_fields):

        if not user_email:
            raise ValueError(_('You must provide an email address'))

        user_email       =   self.normalize_email(user_email)
        user             =   self.model(user_email=user_email, user_name=user_name, user_fname=user_fname, user_lname=user_lname, 
                                 **other_fields)
        
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_fname              =       models.CharField(max_length=200, verbose_name='First Name', default='Undefined')
    user_lname              =       models.CharField(max_length=200, verbose_name='Last Name', default='Undefined')
    user_email              =       models.EmailField(_('email address'), max_length=200, default='Undefined@email')
    user_position           =       models.CharField(max_length=200, verbose_name='Position', default='Undefined')
    user_branch             =       models.CharField(max_length=100, verbose_name='User Branch', default='Undefined')
    user_name               =       models.CharField(max_length=100, verbose_name='User Name', unique=True, default='Undefined')
    user_image              =       models.ImageField(upload_to=image_path, default='profile_pic/default_image.png')
    about                   =       models.TextField(_('about'), max_length='300', default='Undefined')
    is_staff                =       models.BooleanField(default=False)
    is_active               =       models.BooleanField(default=False)
    can_selectbranch        =       models.BooleanField(default=False, verbose_name='Can Select Branch')
    can_editclient          =       models.BooleanField(default=True, verbose_name='Can edit client')
    can_accessaws           =       models.BooleanField(default=False)
    can_accessusers         =       models.BooleanField(default=True)
    can_accessclients       =       models.BooleanField(default=True)
    can_accessmmaptsp2      =       models.BooleanField(default=True)
    def image_tag(self):    
        return mark_safe('<img src="/users/media/%s" width="50" height"50" />'%(self.user_image))
    reg_date        = models.DateField(default=now)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['user_email','user_fname', 'user_lname', 'user_branch']

    def __str__(self):
        return self.user_name
        

class Comment(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    name        = models.CharField(max_length=100, blank=True, null=True)
    email       = models.EmailField(default='null')
    body        = models.TextField(default='null')
    created_on  = models.DateTimeField(default=now)
    active      = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
