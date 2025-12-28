from django import forms
from .models import Post, Swap, BuySell, Donation, Category # <--- 1. อย่าลืม import Category

TAILWIND_INPUT = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # 2. เพิ่ม 'category' เข้าไปใน fields
        fields = ['title', 'description', 'category', 'post_type', 'image'] 
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'category': 'หมวดหมู่สินค้า', # <--- เพิ่ม Label
            'post_type': 'ประเภทโพสต์',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
            # 3. เพิ่ม Widget สำหรับเลือก Category
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}), 
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
        }


class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = ['title', 'description', 'category', 'post_type', 'swap_item_description', 'swap_item_category', 'image', 'leaflet_lat', 'leaflet_lng']
        
        labels = {
            'title': 'หัวข้อ (ของที่มี)',
            'description': 'รายละเอียดของที่มี',
            'category': 'หมวดหมู่ (ของที่มี)',
            'post_type': 'ประเภทโพสต์',
            'swap_item_description': 'สิ่งที่อยากได้แลกเปลี่ยน',
            'swap_item_category': 'หมวดหมู่ (ของที่อยากได้)', # <--- เพิ่ม Label
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'ระบุชื่อสิ่งของที่คุณมี'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'บอกรายละเอียดของสภาพสิ่งของ'}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            
            'swap_item_description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':3, 'placeholder': 'ระบุสิ่งที่คุณอยากได้มาแลกเปลี่ยน'}),
            'swap_item_category': forms.Select(attrs={'class': TAILWIND_INPUT}), # <--- เพิ่ม Widget
            
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

class BuySellForm(forms.ModelForm):
    class Meta:
        model = BuySell
        fields = ['title', 'description', 'post_type','category', 'price', 'is_buying', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'post_type': 'ประเภทโพสต์',
            'category': 'หมวดหมู่สินค้า',
            'price': 'ราคา',
            'is_buying': 'ซื้อหรือขาย',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'price': forms.NumberInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกราคา'}),
            'is_buying': forms.CheckboxInput(attrs={'class':'form-checkbox h-5 w-5 text-blue-600'}),
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description','category', 'post_type', 'condition', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'category': 'หมวดหมู่สินค้า',
            'post_type': 'ประเภทโพสต์',
            'condition': 'สภาพของสิ่งของ',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
            'category': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'condition': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':3, 'placeholder': 'ระบุสภาพสิ่งของ'}),
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['condition'].required = False  # ทำให้ optional
