from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account 

# Register your models here.

class AccountAdmin(UserAdmin):
    list_display=('email','first_name','username','last_name','date_joined','last_login','is_active')

    #to ge the link for the fields
    list_display_links=('email','first_name','last_name')

    readonly_fields=('last_login','date_joined')

    # to set the filter for date_joined

    ordering=('-date_joined',)


    #default setting for coustom user
    filter_horizontal=()
    list_filter=()
    fieldsets=()


admin.site.register(Account,AccountAdmin)  