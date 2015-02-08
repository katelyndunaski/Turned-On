from django.contrib import admin
from backendStuffs.models import *

# admin.site.register(UserPhone)
# # admin.site.register(Regions)
# admin.site.register(UserinGroup)
# Register your models here.

class UserPhoneAdmin(admin.ModelAdmin):
    list_display = ['name','phone_number','region']

class UserinGroupAdmin(admin.ModelAdmin):
    list_display = ['name', "region"]

admin.site.register(UserPhone, UserPhoneAdmin)
admin.site.register(UserinGroup, UserinGroupAdmin)
