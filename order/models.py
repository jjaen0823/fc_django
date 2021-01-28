from django.db import models

# Create your models here.


class Order(models.Model):
    # models.ForeignKey('app_name.class_name', on_delete=models_CASCADE)
    fcuser = models.ForeignKey(
        'fcuser.Fcuser', on_delete=models.CASCADE, verbose_name='User')
    product = models.ForeignKey(
        'product.Product', on_delete=models.CASCADE, verbose_name='Product')
    quantity = models.IntegerField(verbose_name='Product Quantity')
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Register Date")

    def __str__(self):
        return str(self.fcuser) + ' ' + str(self.product)

    class Meta:
        db_table = 'fc_order'
        verbose_name = 'order'
        verbose_name_plural = 'order'
