# requests/models.py
from django.db import models
from django.conf import settings
from posts.models import Post # This model seems to be the one you're using for 'Product'

class Request(models.Model):
    REQUEST_TYPES = (
        ('swap', 'แลกของ'),
        ('buy_sell', 'ขาย/รับซื้อ'),
        ('donate', 'บริจาค'),
    )
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='requests')
    request_type = models.CharField(max_length=10, choices=REQUEST_TYPES)
    message = models.TextField(blank=True) # Change to allow blank for simplicity
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'รอดำเนินการ'), ('accepted', 'Accepted'), ('rejected', 'Rejected')],
        default='pending'
    )
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='requests_made')
    
    # New fields for different request types
    offered_product = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='offered_for_trade')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    reason = models.TextField(blank=True)

    def __str__(self):
        return f"Request by {self.requester} for {self.post} - Status: {self.status}"