from django.contrib import admin
from .models import Account, Destination
# Register your models here.

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_id', 'name', 'app_secret_token')
    search_fields = ('email', 'name')
    
@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('account', 'url', 'http_method')
    search_fields = ('url', 'account__name')