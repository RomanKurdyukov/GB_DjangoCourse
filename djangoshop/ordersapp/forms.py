from django import forms

from mainapp.models import Product
from ordersapp.models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(
        label='цена',
        required=False,
        # widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = Order
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        super(OrderItemForm, self).__init__(*args, **kwargs)

        self.fields['product'].queryset = Product.objects.filter(quantity__gte=1)


