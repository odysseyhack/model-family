from django.contrib import admin

from .models import HNPclient.pyOAuth


@admin.register(HNPOAuth)
class HNPOAuthAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'token')
