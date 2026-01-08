from django.db import models
from django.conf import settings

class Notification(models.Model):
    
    CHOICES = (
        ('system', 'System Alert'),
        ('message', 'New Message'),
    )
    
    recipient = models.ForeignKey(
            settings.AUTH_USER_MODEL, 
            on_delete=models.CASCADE, 
            related_name='notifications'
        )
    message = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.recipient.username}: {self.message}"