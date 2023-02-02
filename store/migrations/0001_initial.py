# Generated by Django 4.1.4 on 2023-02-01 10:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('genre', '0001_initial'),
        ('artist', '0001_initial'),
        ('medium', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artwork',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('artwork_title', models.CharField(max_length=500)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('height', models.DecimalField(decimal_places=2, max_digits=5)),
                ('width', models.DecimalField(decimal_places=2, max_digits=5)),
                ('description', models.TextField(blank=True, max_length=1000)),
                ('is_verified', models.BooleanField(default=True)),
                ('price', models.IntegerField()),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
                ('image', models.ImageField(upload_to='photos/artworks')),
                ('artist_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='artist.artist')),
                ('genre', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='genre.genre')),
                ('medium_title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medium.medium')),
            ],
        ),
    ]
