import uuid
from django.db import models

ROLES = [('admin','Admin'),('member','Member'),('viewer','Viewer')]

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)