from django.db import models
from django.conf import settings
from posts.models import Post
# Create your models here.

class Request(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='requests')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'รอดำเนินการ'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests_made')

    def __str__(self):
        return f"Request by {self.requester} for {self.post} - Status: {self.status}"   
