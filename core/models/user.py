import uuid
import bcrypt
from django.db import models

ROLES = [('admin','Admin'),('member','Member'),('viewer','Viewer')]

class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('core.Company', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, default='')
    role = models.CharField(max_length=20, choices=ROLES, default='member')
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = bcrypt.hashpw(
            raw_password.encode('utf-8'),
            bcrypt.gensalt()
        ).decode('utf-8')

    def check_password(self, raw_password):
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password.encode('utf-8')
        )