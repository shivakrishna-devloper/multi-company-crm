from .base import TenantModel
from django.db import models

class Project(TenantModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    class Meta:
        db_table = 'projects'