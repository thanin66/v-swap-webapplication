# requests/forms.py
from django import forms
from posts.models import Post

class SwapRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False, label="ข้อความ")
    offered_product = forms.ModelChoiceField(queryset=Post.objects.none(), label="สินค้าที่คุณต้องการแลก")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Assumes Post model has a 'type' field and a 'owner' field
            self.fields['offered_product'].queryset = Post.objects.filter(owner=user, post_type='swap')

class SaleRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False, label="ข้อความ")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="จำนวนเงินที่เสนอ")

class DonateRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, required=True, label="เหตุผลที่ต้องการ")