# Generated by Django 4.1.5 on 2023-01-04 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medium',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medium_title', models.CharField(max_length=400)),
                ('slug', models.SlugField(max_length=500, unique=True)),
                ('description', models.TextField(blank=True, max_length=1000)),
            ],
        ),
    ]
