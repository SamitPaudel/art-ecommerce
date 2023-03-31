from django.db.models.signals import post_save
from django.dispatch import receiver

from artist.models import Artist
from .models import ArtPortfolio
from accounts.models import Account

@receiver(post_save, sender=ArtPortfolio)
def approve_artist(sender, instance, **kwargs):
    if instance.isApproved and not instance.artist.is_verified_artist:
        # update the Account object
        instance.artist.is_verified_artist = True
        instance.artist.save()
        # create a new Artist object
        artist = Artist.objects.create(
            artist_email=instance.artist,
            artist_name=instance.artist.full_name,
            slug=instance.artist.username,
            description='',
        )