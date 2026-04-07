
import uuid
from django.db import models

class TenantManager(models.Manager):
    def for_tenant(self, company_id):
        return self.get_queryset().filter(company_id=company_id)

class TenantModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = TenantManager()
    class Meta:
        abstract = True