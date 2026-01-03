# requests/forms.py
from django import forms
from posts.models import Post

class SwapRequestForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, required=False, label="ข้อความ")
    offered_product = forms.ModelChoiceField(queryset=Post.objects.none(), label="สินค้าที่คุณต้องการแลก")
    

    def clean_offered_product(self):
        product = self.cleaned_data.get('offered_product')
        # ตรวจสอบว่า User เป็นเจ้าของของชิ้นที่เอามาเสนอจริงไหม
        # self.initial['user'] ต้องถูกส่งมาตอน init form หรือดึงจาก request ใน view แทน
        # แต่วิธีที่ง่ายที่สุดคือ เช็คใน View.py ตอนรับ POST ครับ (ดูข้อถัดไป)
        return product
        
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