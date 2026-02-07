from django import forms
from .models import Post, Swap, BuySell, Donation, Category

# กำหนด Style ให้ Input สวยงามตาม Tailwind
TAILWIND_INPUT = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400 transition'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'category', 'post_type', 'image']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'category': 'หมวดหมู่สินค้า',
            'post_type': 'ประเภทโพสต์',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'หัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows': 4, 'placeholder': 'รายละเอียด...'}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
        }

class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = ['title', 'description', 'category' , 'swap_item_description', 'swap_item_category', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'ของที่จะแลก',
            'description': 'รายละเอียดของสภาพของ',
            'category': 'หมวดหมู่ของที่จะแลก',
            'swap_item_description': 'รายละเอียดของที่อยากได้',
            'swap_item_category': 'หมวดหมู่ของที่อยากได้',
            'image': 'รูปภาพของจริง',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'เช่น กีตาร์โปร่ง Yamaha'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows': 4}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'swap_item_description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows': 3, 'placeholder': 'ระบุสิ่งที่อยากได้มาแลก...'}),
            'swap_item_category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

# --- [ใหม่] ฟอร์มสำหรับลงขาย (Sale) ---
class SaleForm(forms.ModelForm):
    class Meta:
        model = BuySell
        fields = ['title', 'description', 'price', 'category', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'ชื่อสินค้า',
            'description': 'รายละเอียดสภาพสินค้า',
            'price': 'ราคาขาย (บาท)',
            'category': 'หมวดหมู่',
            'image': 'รูปถ่ายสินค้าจริง',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'ชื่อสินค้าที่ต้องการขาย'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows': 4, 'placeholder': 'สภาพสินค้า ตำหนิ การจัดส่ง...'}),
            'price': forms.NumberInput(attrs={'class': TAILWIND_INPUT}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

    # บังคับให้คนขายต้องใส่รูปสินค้าเสมอ เพื่อความน่าเชื่อถือ
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

# --- [ใหม่] ฟอร์มสำหรับประกาศตามหา (Wishlist) ---
class WishlistForm(forms.ModelForm):
    class Meta:
        model = BuySell
        fields = ['title', 'description', 'price', 'category', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'สิ่งที่กำลังตามหา',
            'description': 'รายละเอียดที่ต้องการ',
            'price': 'งบประมาณสูงสุด (บาท)', # เปลี่ยน Label ให้สื่อความหมาย
            'category': 'หมวดหมู่',
            'image': 'รูปภาพตัวอย่าง (ถ้ามี)',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'เช่น ตามหา iPhone 13 มือสอง'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows': 4, 'placeholder': 'ระบุสี รุ่น สภาพที่รับได้...'}),
            'price': forms.NumberInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'ระบุงบที่มี'}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'category', 'condition', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'ของที่จะบริจาค',
            'description': 'รายละเอียด',
            'category': 'หมวดหมู่',
            'condition': 'สภาพของสิ่งของ',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'เช่น เสื้อผ้ามือสอง หนังสือเรียน'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows': 4}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'condition': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'เช่น ใช้งานได้ปกติ, เก่าเก็บ'}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }