from django.db import models
from django.conf import settings
from imagekit.models import ProcessedImageField


class Account(models.Model):
    CHOICES = [('DA', '아빠'), ('MO', '엄마'), ('1S', '첫째'), ('2S', '둘째'),
               ('3S', '셋째')]
    user = models.OneToOneField(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE)
    name = models.CharField(max_length=10, default="")
    role = models.CharField(max_length=2, choices=CHOICES, null=True)
    family_id = models.IntegerField(null=False, default=-1)
    phone_number = models.CharField(max_length=11, null=True)
    notifications = models.TextField(
        default="[]")  # '[{"name":"yeongyu", "family_id":1}]'
    image = ProcessedImageField(upload_to='media/%Y-%m-%d/',
                                format='JPEG',
                                options={'quality': 60},
                                blank=True,
                                default="")
