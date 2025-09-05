from django import forms
from .models import Post, Swap, BuySell, Donation

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_type', 'image']

class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = ['title', 'description', 'post_type', 'swap_item_description', 'image']
    
class BuySellForm(forms.ModelForm):
    class Meta:
        model = BuySell
        fields = ['title', 'description', 'post_type', 'price', 'is_buying', 'image']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['title', 'description', 'post_type', 'condition', 'image']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['condition'].required = False  # Make condition optional
