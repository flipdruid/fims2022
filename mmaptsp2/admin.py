from django.contrib import admin
from .models import Mmap, Beneficiary, Sccn, Branchcode

# Register your models here.


class MmapAdmin(admin.ModelAdmin):
    list_display = ['id', 'clientid','mmap_name', 'mmap_branch', 'mmap_setupdate', 'mmap_age', 'mmap_type', 'mmap_premium', 'mmap_sex',  'client_cycle', 'mmapservicecentercontrolno']
    search_fields = ['mmap_name', 'mmap_branch','id', 'mmapservicecentercontrolno']


class BeneficiaryAdmin(admin.ModelAdmin):
    list_display = ['id','mmapid', 'ben_mmap_name', 'mmap_clientid', 'mmapservicecentercontrolno', 'client_cycle', 'ben1', 'ben2', 'ben3']
    search_fields = ['mmapid', 'mmap_clientid', 'ben1', 'ben2', 'ben3', 'mmapservicecentercontrolno']

class SccnAdmin(admin.ModelAdmin):
    list_display = ['id', 'sccnbcode', 'sscnservicecentercontrolno', 'client_name', 'mmap_encodedate', 'mmap_setupdate','mmap_expired']
    search_fields = ['sccnbcode', 'sscnservicecentercontrolno']

class BranchcodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'bcode', 'bname', 'dateadded']
    search_fields = ['bcode', 'bname']

admin.site.register(Mmap, MmapAdmin)
admin.site.register(Beneficiary, BeneficiaryAdmin)
admin.site.register(Sccn, SccnAdmin)
admin.site.register(Branchcode, BranchcodeAdmin)