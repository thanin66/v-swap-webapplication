from django.db import models
from django.conf import settings

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, allow_unicode=True)

    def __str__(self):
        return self.name
    
class Post(models.Model):
    POST_TYPES = [
        ('swap', 'แลกของ'),
        ('buy_sell', 'ขาย/รับซื้อ'),
        ('donate', 'ให้ฟรี'),
    ]
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPES)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    status = models.CharField(max_length=50, default='available')


    created_at = models.DateTimeField(auto_now_add=True)
    leaflet_lat = models.FloatField(blank=True, null=True)
    leaflet_lng = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"[{self.get_post_type_display()}] {self.title}"

class Swap(Post):
    swap_item_description = models.TextField()
    swap_item_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='swap_posts')

class BuySell(Post):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_buying = models.BooleanField(default=False)  

class Donation(Post):
    condition = models.CharField(max_length=255, blank=True) 


class PostReport(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports_made')
    reason = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


