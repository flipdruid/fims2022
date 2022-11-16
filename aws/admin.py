from django.contrib import admin

from .models import Aws, Awsaccounts
# Register your models here.


class AwsaccountsAdmin(admin.ModelAdmin):
    list_display = ['id', 'accountName','accountID', 'accountUser', 'accessKeyID', 'secretAccessKey',
        'region']

class AwsAdmin(admin.ModelAdmin):
    list_display = ['id', 'accountName','accountID', 'accountUser', 'accessKeyID', 'secretAccessKey', 'instanceName', 'instanceID', 
        'region',  'database', 'serverType']
    # search_fields = ['mmap_name', 'mmap_branch','id', 'mmapservicecentercontrolno']



admin.site.register(Aws, AwsAdmin)

admin.site.register(Awsaccounts, AwsaccountsAdmin)