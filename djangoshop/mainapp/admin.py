from django.contrib import admin
from .models import *


# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('vendor_code',
                    'name',
                    'category',
                    'price'
                    )

class ImageAdmin(admin.ModelAdmin):
    list_display = ('vendor_code',
                    'date'
                    )


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Image,ImageAdmin)
admin.site.register(VendorCode)
