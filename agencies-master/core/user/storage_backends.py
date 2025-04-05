import os

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from django_tenants.utils import get_tenant


class TenantS3Storage(S3Boto3Storage):
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        tenant = get_tenant(request=request) if request else None
        if tenant and tenant.schema_name != 'public':
            self.location = f'media/{tenant.schema_name}'
        else:
            self.location = settings.AWS_LOCATION
        super().__init__(*args, **kwargs)

    def _save(self, name, content):
        self.location = self.get_location()
        # Extract the filename from the name argument
        # filename = name.split('/')[-1]
        # # Construct the full path based on the location and filename
        # full_path = os.path.join(self.location, filename)
        return super()._save(name, content)

    def get_location(self):
        request = self._request()
        print('request', request)
        tenant = get_tenant(request=request) if request else None
        print('tenant', tenant)
        if tenant and tenant.schema_name != 'public':
            return f'media/{tenant.schema_name}'
        else:
            return settings.AWS_LOCATION

    def url(self, name, query_auth=True, expire=None):
        self.location = self.get_location()
        return super().url(name, query_auth, expire)

    def _request(self):
        from django.utils.deprecation import MiddlewareMixin
        if hasattr(MiddlewareMixin, '_thread_local'):
            return getattr(MiddlewareMixin._thread_local, 'request', None)
        return None
