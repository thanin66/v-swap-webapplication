# requests/forms.py
from django import forms
from posts.models import Post

class SwapRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False, label="ข้อความ")
    offered_product = forms.ModelChoiceField(queryset=Post.objects.none(), label="สินค้าที่คุณต้องการแลก")
    

    def clean_offered_product(self):
            product = self.cleaned_data.get('offered_product')
            # เช็คเพิ่มเติมเผื่อผ่านหน้า Form มาได้ แต่สถานะเปลี่ยนพอดี
            if product and product.status == 'completed':
                raise forms.ValidationError("สินค้านี้ได้ถูกแลกเปลี่ยนไปแล้ว ไม่สามารถนำมาเสนอได้อีก")
            return product
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Assumes Post model has a 'type' field and a 'owner' field
            self.fields['offered_product'].queryset = Post.objects.filter(
                            owner=user, 
                            post_type='swap'
                        ).exclude(status='completed')
class SaleRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False, label="ข้อความ")
    amount = forms.DecimalField(max_digits=10, decimal_places=2, label="จำนวนเงินที่เสนอ")

class DonateRequestForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea, required=True, label="เหตุผลที่ต้องการ")