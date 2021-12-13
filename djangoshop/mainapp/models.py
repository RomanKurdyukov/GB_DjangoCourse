from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete, post_save
from django.core.cache import cache


class ProductCategory(models.Model):
    """категории товаров"""
    name = models.CharField(
        verbose_name='имя',
        max_length=64,
        unique=True
    )

    description = models.TextField(
        verbose_name='описание',
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name='создано',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='изменено',
        auto_now=True
    )

    is_active = models.BooleanField(verbose_name='активна', default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name', '-created_at']


class VendorCode(models.Model):

    code = models.DecimalField(
        max_digits=8,
        decimal_places=0,
        verbose_name='артикул'
    )

    def __str__(self):
        return f'{self.code}'

    class Meta:
        verbose_name = 'артикул'
        verbose_name_plural = 'артикулы'
        ordering = ['code']


class Image(models.Model):
    """изображения товаров"""
    vendor_code = models.ForeignKey(
        VendorCode,
        verbose_name='артикул товара',
        on_delete=models.CASCADE,
    )

    image = models.ImageField(
        upload_to='products_images',
        verbose_name='фото',
        blank=True
    )

    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата'
    )
    short_description = models.CharField(
        max_length=127,
        verbose_name='краткое описание',
        blank=True
    )

    def __str__(self):
        return f'{self.vendor_code.code}'

    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фото товаров'
        ordering = ['vendor_code', '-date']


class Product(models.Model):
    """товары"""
    image = models.ForeignKey(
        Image,
        on_delete=models.SET_NULL,
        verbose_name='фото',
        blank=True,
        null=True
    )

    category = models.ForeignKey(
        ProductCategory,
        on_delete=models.CASCADE,
        verbose_name='категория'
    )
    vendor_code = models.ForeignKey(
        VendorCode,
        verbose_name='артикул товара',
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=128,
        verbose_name='наименование'
    )

    short_desc = models.CharField(
        verbose_name='краткое описание',
        max_length=64,
        blank=True
    )

    description = models.TextField(
        verbose_name='описание товара',
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='цена'
    )

    quantity = models.PositiveIntegerField(
        default=0,
        verbose_name='количество'
    )

    is_active = models.BooleanField(verbose_name='активна', default=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} {self.vendor_code} ({self.category.name})'


    class Meta:
        verbose_name = 'Товара'
        verbose_name_plural = 'Товары'
        ordering = ['vendor_code', '-created_at']


# def model_post_save(sender, instance, *args, **kwargs):
#     cache.clear()
#     print('cache_is_cleared')
#
#
# post_save.connect(model_post_save, sender=Product)
