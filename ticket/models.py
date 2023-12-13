from django.db import models
import uuid


class Ticket(models.Model):

    token = models.UUIDField(default=uuid.uuid4, db_index=True)
    is_regenerate = models.BooleanField(default=False)
