from django.db import models

class User(models.Model):
    date_of_registration = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        db_table = 'users'
        ordering = ['id']
