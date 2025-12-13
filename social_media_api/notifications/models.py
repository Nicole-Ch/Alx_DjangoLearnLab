from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actors")
    verb = models.CharField(max_length=100)
    timestamp = models.TimeField(auto_now_add=True)
    target_content_type = models.ForeignKey(ContentType, on_delete = models.CASCADE, null=True, blank=True )
    target_object_id = models.PositiveBigIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_content_type', 'target_object_id')

    def __str__(self):
        return f"{self.actor} {self.verb} -> {self.recipient} ({self.target})"
    
    class Meta:
        ordering = ['-timestamp']