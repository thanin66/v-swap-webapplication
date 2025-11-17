from django import forms
from .models import Post, Swap, BuySell, Donation

TAILWIND_INPUT = 'w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-400'

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_type', 'image']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'post_type': 'ประเภทโพสต์',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
        }

class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = ['title', 'description', 'post_type', 'swap_item_description', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'post_type': 'ประเภทโพสต์',
            'swap_item_description': 'รายละเอียดของที่จะแลก',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
            'swap_item_description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':3, 'placeholder': 'รายละเอียดสิ่งของที่จะแลก'}),
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

class BuySellForm(forms.ModelForm):
    class Meta:
        model = BuySell
        fields = ['title', 'description', 'post_type', 'price', 'is_buying', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'post_type': 'ประเภทโพสต์',
            'price': 'ราคา',
            'is_buying': 'ซื้อหรือขาย',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
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
        fields = ['title', 'description', 'post_type', 'condition', 'image', 'leaflet_lat', 'leaflet_lng']
        labels = {
            'title': 'หัวข้อ',
            'description': 'รายละเอียด',
            'post_type': 'ประเภทโพสต์',
            'condition': 'สภาพของสิ่งของ',
            'image': 'รูปภาพ',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': TAILWIND_INPUT, 'placeholder': 'กรอกหัวข้อโพสต์'}),
            'description': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':4, 'placeholder': 'กรอกรายละเอียดโพสต์'}),
            'condition': forms.Textarea(attrs={'class': TAILWIND_INPUT, 'rows':3, 'placeholder': 'ระบุสภาพสิ่งของ'}),
            'post_type': forms.Select(attrs={'class': TAILWIND_INPUT}),
            'image': forms.ClearableFileInput(attrs={'class': TAILWIND_INPUT}),
            'leaflet_lat': forms.HiddenInput(),
            'leaflet_lng': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['condition'].required = False  # ทำให้ optional
