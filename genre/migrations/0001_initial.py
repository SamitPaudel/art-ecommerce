# Generated by Django 4.1.4 on 2023-02-01 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400)),
                ('slug', models.SlugField(max_length=500, unique=True)),
                ('description', models.TextField(blank=True, max_length=1000)),
            ],
        ),
    ]
