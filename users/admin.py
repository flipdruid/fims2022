from django.contrib import admin
from .models import User, Comment
from django.contrib.contenttypes.admin import GenericTabularInline
from django.forms import Textarea


admin.site.site_header="KMSystem User Area"
admin.site.site_title="KMSystem User Area"
admin.site.index_title="Welcome to KMSystem User Area"

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0

class UserAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'user_name', 'user_fname', 'user_lname', 'user_email', 'user_branch', 'user_position', 'can_accessaws']
    # ordering = ()
    list_filter = ('user_email', 'user_name', 'is_active', 'is_superuser','is_staff')
    search_fields = ['user_fname', 'user_lname', 'user_email', 'user_position']

    fieldsets = (
                # (None, {'fields': ('user_email', 'user_name', 'user_fname', 'user_lname',)}),
                (None, {'fields': ('user_email', 'user_name','user_branch')}),
                ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser','can_selectbranch','can_editclient', 
                'can_accessaws', 'can_accessusers', 'can_accessclients', 'can_accessmmaptsp2')}),
                ('Personal', {'fields': ('about',)}),
                )

    formfield_overrides = {
        User.about: {'widget': Textarea(attrs={'rows': 10, 'cols': 40})},
    }

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_email', 'user_name', 'user_fname', 'user_lname', 'password1', 
            'password2', 'is_staff', 'is_active')
        }
        ))

    # inlines = [CommentInline]

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'user_id', 'created_on', 'active')
    list_filter= ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comment']

    def approve_comment(self, request, queryset):
        queryset.update(active=True)    

admin.site.register(User, UserAdmin)
admin.site.register(Comment, CommentAdmin)