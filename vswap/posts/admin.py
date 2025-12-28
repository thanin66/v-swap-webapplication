from django.contrib import admin
from .models import Post, Swap, BuySell, Donation, Category

# 1. ส่วนของ Category (ที่คุณเพิ่งทำ)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug')

# 2. ส่วนของ Post (ของเดิมที่มีอยู่แล้ว เก็บไว้แบบนี้)
# ถ้ามี @admin.register(Post) อยู่แล้ว ห้ามมี admin.site.register(Post) อีก
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'post_type', 'status', 'created_at']
    # ... โค้ดเดิมของคุณ ...

# 3. ส่วนของ Model อื่นๆ
# ถ้า model ไหนยังไม่มี class Admin ให้ใช้บรรทัดล่างนี้ได้
# แต่ถ้ามี class @admin.register(...) แล้ว ให้ลบบรรทัดพวกนี้ทิ้งครับ
admin.site.register(Swap)     # <-- ถ้าข้างล่างมี SwapAdmin ให้ลบบรรทัดนี้
admin.site.register(BuySell)  # <-- ถ้าข้างล่างมี BuySellAdmin ให้ลบบรรทัดนี้
admin.site.register(Donation) # <-- ถ้าข้างล่างมี DonationAdmin ให้ลบบรรทัดนี้