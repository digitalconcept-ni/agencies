from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from client.models import Client, Domain


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'schema_name')


@admin.register(Domain)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ('domain',)
