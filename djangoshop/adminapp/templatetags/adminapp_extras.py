from django import template

from mainapp.models import Product, ProductCategory

register = template.Library()


@register.simple_tag
def prod_counter(pk):
    products_set = Product.objects.filter(category=pk).count()
    return products_set


@register.simple_tag
def current_cat(request):
    path = request.path
    return int(''.join(path[36:37]))


@register.simple_tag
def current_name(request):
    path = request.path
    cat_id = int(''.join(path[36:37]))
    cat_name = ProductCategory.objects.filter(id=cat_id).values_list('name', flat=True)[0]
    return cat_name
