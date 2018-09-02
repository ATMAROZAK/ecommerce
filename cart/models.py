from django.db import models

# Create your models here.

class Shipping(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description = models.CharField(max_length=50)

    defaullt = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

        verbose_name = 'Доставка'
        verbose_name_plural = 'Доставки'

    def __str__(self):
        return self.name