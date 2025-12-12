from django.db import models
from django.conf import settings
# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recipients")
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="actors")
    verb = models.CharField(max_length=100)
    target = models.CharField(max_length=100)
    timestamp = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.actor} {self.verb}"
    
    class Meta:
        ordering = ['-timestamp']