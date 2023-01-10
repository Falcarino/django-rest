import os
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]  # can also be emtpy if it's your first migration

    def generate_superuser(apps, schema_editor):
        from users.models import User
        from products.models import Product
        from tests.factories import ProductFactory

        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', 'lkjfsdg@gmail.com')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', '12345apcfd')

        superuser = User.objects.create_superuser(
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD
        )

        superuser.save()

        for _ in range(3):
            ProductFactory.create(user_id=superuser)

    operations = [
        migrations.RunPython(generate_superuser),
    ]
