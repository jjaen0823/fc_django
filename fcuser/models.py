from django.db import models

# Create your models here.


class Fcuser(models.Model):
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=64, verbose_name='Password')
    register_date = models.DateTimeField(
        auto_now_add=True, verbose_name='Register Date')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'fc_fcuser'
        verbose_name = 'fcuser'
        verbose_name_plural = 'fcuser'
