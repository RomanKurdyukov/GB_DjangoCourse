from authapp.models import ShopUser
from authapp.forms import ShopUserEditForm, ProductCategoryEditForm
from mainapp.models import ProductCategory


class ShopUserAdminEditForm(ShopUserEditForm):
    class Meta:
        model = ShopUser
        fields = '__all__'


class ProductCategoryAdminEditForm(ProductCategoryEditForm):
    class Meta:
        model = ProductCategory
        fields = '__all__'
