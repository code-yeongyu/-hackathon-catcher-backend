from django.db import models
from django.conf import settings
from family.models import Family


class Account(models.Model):
    CHOICES = [('DA', '아빠'), ('MO', '엄마'), ('1S', '첫째'), ('2S', '둘째'),
               ('3S', '셋째')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    role = models.CharField(max_length=2, choices=CHOICES, null=True)
    family = models.ForeignKey(Family, on_delete=models.CASCADE, null=True)
    phone_number = models.CharField(max_length=11, null=True)