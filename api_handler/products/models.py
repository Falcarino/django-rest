from django.db import models

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey('User', on_delete=models.CASCADE)

    product_type = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    model = models.CharField(max_length=30)

    class Meta:
        db_table = 'products'
        ordering = ['product_id']
