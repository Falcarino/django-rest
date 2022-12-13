from django.db import models
from django.utils.translation import gettext_lazy as _



class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product_type = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    date_of_registration = models.DateTimeField(auto_now_add=True)
    date_of_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering = ['product_id']
