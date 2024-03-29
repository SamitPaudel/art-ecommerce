# Generated by Django 4.1.4 on 2023-02-17 11:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_delete_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtPortfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('image1', models.ImageField(blank=True, null=True, upload_to='art_portfolio_images')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='art_portfolio_images')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='art_portfolio_images')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='art_portfolio_images')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='art_portfolio_images')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
