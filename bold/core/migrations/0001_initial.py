import os
from django.db import migrations
from django.conf import settings


class Migration(migrations.Migration):
    """
        Initial migration to populate the database
    """

    initial = True

    dependencies = [
    ]

    def generate_superuser(apps, schema_editor):
        from django.contrib.auth.models import User
        superuser = User.objects.create_superuser(
            username=settings.DEFAULT_ADMIN_CREDENTIALS.get('username'),
            email=settings.DEFAULT_ADMIN_CREDENTIALS.get('email'),
            password=settings.DEFAULT_ADMIN_CREDENTIALS.get('password')
        )

        superuser.save()

    operations = [
        migrations.RunPython(generate_superuser),
    ]