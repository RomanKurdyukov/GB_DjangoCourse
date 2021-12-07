from django.conf import settings
from django.db import models

from mainapp.models import Product


class BasketQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()
        super(BasketQuerySet, self).delete()


class Basket(models.Model):
    objects = BasketQuerySet.as_manager()

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

    is_active = models.BooleanField(verbose_name='активна', default=True)

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

    @staticmethod
    def get_items(user):
        return Basket.objects.filter(user=user)

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_qty(self):
        _items = Basket.objects.filter(user=self.user)
        _total_qty = sum(list(map(lambda x: x.quantity, _items)))
        return _total_qty

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_cost, _items)))
        return _total_cost

    def delete(self):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete()

    def save(self, *args, **kwargs):
        if self.pk:
            self.product.quantity -= self.quantity - self.__class__.get_item(self.pk).quantity
        else:
            self.product.quantity -= self.quantity
        self.product.save()
        super(self.__class__, self).save(*args, **kwargs)



    def __str__(self):
        return f'Корзина: {self.user}, Товар: {self.product}'

    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзина'
        ordering = ['user', '-created_at']
