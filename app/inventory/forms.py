from django import forms
from .models import Products


class ProductForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop("instance", None)
        super().__init__(*args, **kwargs)

    name = forms.CharField(
        max_length=200,
        required=True,
        error_messages={
            "max_length": "商品名は最大200文字です",
            "required": "商品名は必須です",
        },
    )
    sku = forms.CharField(
        max_length=50,
        required=True,
        error_messages={
            "max_length": "SKUは最大50文字です",
            "required": "SKUは必須です",
        },
    )
    description = forms.CharField(
        max_length=1000,
        required=False,
        error_messages={
            "max_length": "商品説明は最大1,000文字です",
        },
    )
    price = forms.CharField(
        required=True,
        error_messages={
            "required": "価格は必須です",
        },
    )
    quantity = forms.IntegerField(
        min_value=0,
        error_messages={
            "required": "在庫数は必須です",
            "min_value": "在庫数には0より小さい値を設定できません",
        },
    )

    def clean_price(self):
        price_str = self.cleaned_data["price"]
        try:
            price_int = int(price_str.replace(",", ""))
        except Exception:
            raise forms.ValidationError("価格には正常な値を入力してください")
        if price_int < 0:
            raise forms.ValidationError("価格には正常な値を入力してください")
        return price_int

    def clean_sku(self):
        sku = self.cleaned_data["sku"]
        qs = Products.objects.filter(sku=sku)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("入力されたSKUはすでに使用されています")
