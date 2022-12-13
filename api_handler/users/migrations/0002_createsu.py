import os
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]  # can also be emtpy if it's your first migration

    def generate_superuser(apps, schema_editor):
        from users.models import User

        DJANGO_SU_EMAIL = os.environ.get('DJANGO_SU_EMAIL', 'lkjfsdg@gmail.com')
        DJANGO_SU_PASSWORD = os.environ.get('DJANGO_SU_PASSWORD', '12345apcfd')

        superuser = User.objects.create_superuser(
            email=DJANGO_SU_EMAIL,
            password=DJANGO_SU_PASSWORD
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]