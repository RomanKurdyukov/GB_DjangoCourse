from django.core.management.base import BaseCommand

import json
import os

from authapp.models import ShopUser
# from mainapp.sqlutils import reset_incr
from mainapp.models import *
JSON_PATH = 'mainapp/jsons'


def load_from_json(file_name):
    with open(os.path.join(JSON_PATH, file_name + '.json'), mode='r', encoding='utf8') as infile:
        return json.load(infile)


class Command(BaseCommand):
    def handle(self, *args, **options):
        vendor_codes = load_from_json('vendor_codes')
        VendorCode.objects.all().delete()
        # reset_incr.reset_vc()
        for code in vendor_codes:
            new_vendor_code = VendorCode(**code)
            new_vendor_code.save()

        images = load_from_json('images')

        Image.objects.all().delete()
        # reset_incr.reset_img()
        for image in images:
            code_link = image['vendor_code']
            _code_link = VendorCode.objects.get(code=code_link)
            image['vendor_code'] = _code_link
            new_image = Image(**image)
            new_image.save()

        categories = load_from_json('categories')

        ProductCategory.objects.all().delete()
        # reset_incr.reset_prodcat()
        for category in categories:
            new_category = ProductCategory(**category)
            new_category.save()

        products = load_from_json('products')

        Product.objects.all().delete()
        # reset_incr.reset_product()
        for product in products:
            code_link = product['vendor_code']
            _code_link = VendorCode.objects.get(code=code_link)
            product['vendor_code'] = _code_link
            image_name = product['image']
            _image = Image.objects.get(short_description=image_name)
            product['image'] = _image
            category_name = product['category']
            _category = ProductCategory.objects.get(name=category_name)
            product['category'] = _category
            new_product = Product(**product)
            new_product.save()

        ShopUser.objects.all().delete()
        super_user = ShopUser.objects.create_superuser('admin', 'admin@admin.local', 'admin', age=37)
        if super_user:
            print('Admin account successfully created!')
