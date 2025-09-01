from django import forms
from .models import Post, Swap, BuySell, Donation

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'image', 'category']

class SwapForm(forms.ModelForm):
    class Meta:
        model = Swap
        fields = PostForm.Meta.fields + ['offered_item', 'desired_item']

class BuySellForm(forms.ModelForm):
    class Meta:
        model = BuySell
        fields = PostForm.Meta.fields + ['price']

class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = PostForm.Meta.fields + [] 