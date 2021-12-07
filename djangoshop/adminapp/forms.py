from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm, ProductCategoryEditForm, VcAddForm
from mainapp.models import ProductCategory, VendorCode
from django import forms


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryAdminEditForm(ProductCategoryEditForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'


class VcAdminAddForm(VcAddForm):
    class Meta:
        model = VendorCode
        fields = '__all__'


