from django.db import models
from django.conf import settings

class Post(models.Model):
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    POST_TYPES = [
        ('swap', 'แลกของ'),
        ('buy_sell', 'ขาย/รับซื้อ'),
        ('donate', 'บริจาค'),
    ]

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title}"


class Swap(Post):
    swap_item_description = models.TextField()
    # ไม่ต้องเก็บ requester ที่นี่
    # เพราะโพสต์นึงจะมีหลาย request

class SwapRequest(models.Model):
    post = models.ForeignKey(Swap, on_delete=models.CASCADE, related_name="requests")
    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="swap_requests")
    offered_item_description = models.TextField()  # ของที่นำมาแลก
    message = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)


class BuySell(Post):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_buying = models.BooleanField(default=False)  # True=รับซื้อ, False=ขาย


class Donation(Post):
    condition = models.CharField(max_length=255, blank=True)  # เงื่อนไขการรับบริจาค
