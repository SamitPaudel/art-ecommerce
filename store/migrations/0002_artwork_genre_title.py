# Generated by Django 4.1.4 on 2022-12-25 03:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('genre', '0001_initial'),
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='artwork',
            name='genre_title',
            field=models.ForeignKey(default='Modern', on_delete=django.db.models.deletion.CASCADE, to='genre.genre'),
        ),
    ]
