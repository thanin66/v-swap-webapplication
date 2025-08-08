from django.db import models
from django.conf import settings

class Post(models.Model):
    POST_TYPES = [
        ('sell', 'ขาย'),
        ('trade', 'แลก'),
        ('donate', 'บริจาค'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts")
    title = models.CharField(max_length=255)
    description = models.TextField()
    post_type = models.CharField(max_length=10, choices=POST_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # ใช้เฉพาะขาย
    image = models.ImageField(upload_to="post_images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.get_post_type_display()})"
