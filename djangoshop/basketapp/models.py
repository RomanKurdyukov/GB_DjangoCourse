from django.conf import settings
from django.db import models

from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='basket',
        verbose_name='пользователь'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='товар',
    )

    quantity = models.PositiveIntegerField(
        verbose_name='кол-во',
        default=0,
    )

    created_at = models.DateTimeField(verbose_name='время', auto_now_add=True)

    def __str__(self):
        return f'Корзина: {self.user}, Товар: {self.product}'

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзина'
        ordering = ['user', '-created_at']