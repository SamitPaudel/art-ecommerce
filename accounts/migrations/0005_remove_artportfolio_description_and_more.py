# Generated by Django 4.1.4 on 2023-02-17 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_artportfolio'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artportfolio',
            name='description',
        ),
        migrations.RemoveField(
            model_name='artportfolio',
            name='title',
        ),
    ]
