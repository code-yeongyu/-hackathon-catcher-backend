from django.db import models


class Family(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)