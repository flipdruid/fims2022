from django.contrib import admin
from .models import Client, Gender, Civilstat, Product, Membertype, Clientstat, Branch, Clientaccountcode


class ClientAdmin(admin.ModelAdmin):
    list_display = ['id', 'image_tag','client_fname', 'client_mname','client_lname', 'client_code','client_branchcode','client_zipcode', 'client_email', 'client_status', 'client_cycle']

    search_fields = ['client_fname', 'client_lname']

class BranchAdmin(admin.ModelAdmin):
    list_display = ['id','branches']
    search_fields = ['branches']

class ClientaccountcodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'zipcode', 'branchcode', 'branch']
    search_fields = ['zipcode', 'branchcode', 'branch']
    

admin.site.register(Client, ClientAdmin)
admin.site.register(Gender)
admin.site.register(Civilstat)
admin.site.register(Product)
admin.site.register(Membertype)
admin.site.register(Clientstat)
admin.site.register(Branch, BranchAdmin)
admin.site.register(Clientaccountcode, ClientaccountcodeAdmin)