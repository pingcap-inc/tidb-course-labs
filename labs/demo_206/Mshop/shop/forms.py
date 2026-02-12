"""
Forms for shop - validation same as demo_205 Laravel.
"""
from django import forms
from .models import Product


class ProductUpdateForm(forms.ModelForm):
    """Update product (edit) - same rules as Laravel update()."""
    photo_upload = forms.ImageField(required=False, label='Cover')

    class Meta:
        model = Product
        fields = ['status', 'name', 'introduction', 'price', 'remain_count', 'product_type']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-1/2 border border-gray-300 rounded px-3 py-2'}),
            'introduction': forms.Textarea(attrs={'rows': 2, 'maxlength': 200}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'min': '0.1', 'max': '10000'}),
            'remain_count': forms.NumberInput(attrs={'min': 0}),
        }

    def clean_status(self):
        v = self.cleaned_data.get('status')
        if v not in ('C', 'S'):
            raise forms.ValidationError('Invalid status')
        return v

    def clean_price(self):
        v = self.cleaned_data.get('price')
        if v is not None and (v < 0.1 or v > 10000):
            raise forms.ValidationError('Price must be between 0.1 and 10000')
        return v

    def clean_remain_count(self):
        v = self.cleaned_data.get('remain_count')
        if v is not None and v < 0:
            raise forms.ValidationError('Quantity must be >= 0')
        return v

    def save(self, commit=True, photo_path=None):
        inst = super().save(commit=False)
        if photo_path is not None:
            inst.photo = photo_path
        if commit:
            inst.save()
        return inst


class BuyForm(forms.Form):
    """Purchase form - same as Laravel buy() validation."""
    buy_count = forms.IntegerField(min_value=1, required=True)
    pay_with = forms.IntegerField(min_value=1, required=True)
