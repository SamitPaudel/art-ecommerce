# Generated by Django 4.1.4 on 2023-02-22 05:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('artist', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artist',
            name='artist_email',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='artist', to=settings.AUTH_USER_MODEL),
        ),
    ]
