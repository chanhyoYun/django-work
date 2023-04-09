from django import forms
from .models import ProductModel


class ItemForm(forms.ModelForm):
    class Meta:
        model = ProductModel
        fields = '__all__' # 전체 가져오기


