from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'post_type', 'price', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter post description'}),
            'post_type': forms.Select(),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter price (if applicable)'}),
            'image': forms.ClearableFileInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['post_type'].empty_label = "Select post type"