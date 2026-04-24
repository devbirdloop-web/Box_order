from django import forms
from .models import Box


class BoxForm(forms.ModelForm):
    class Meta:
        model = Box
        fields = [
            'name',
            'description',
            'price',
            'stock',
            'image',
            'length',
            'width',
            'height',
            'quality',
            'is_active',
        ]