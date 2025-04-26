import datetime

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import os

class TenantS3Storage(S3Boto3Storage):
    def __init__(self, tenant_prefix=None, *args, **kwargs):
        self.tenant_prefix = tenant_prefix if tenant_prefix and tenant_prefix != 'public' else ''
        self.relative_root = getattr(settings, 'MULTITENANT_RELATIVE_MEDIA_ROOT', '')
        super().__init__(*args, **kwargs)

    def get_location(self):
        month = datetime.datetime.now().strftime("%m")
        return os.path.join(settings.AWS_LOCATION, self.tenant_prefix, month, self.relative_root).lstrip('/')

    def _save(self, name, content):
        self.location = self.get_location()
        return super()._save(name, content)

    def url(self, name, query_auth=True, expire=None):
        self.location = self.get_location()
        return super().url(name, query_auth, expire)