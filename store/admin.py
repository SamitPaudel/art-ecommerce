from django.contrib import admin

# Register your models here.
from store.models import Artwork, ArtworkComment, UserLikedArtwork, Auction, Bid


class ArtworkAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('artwork_title',)
    }
    list_display = ('artwork_title', 'artist_name', 'medium_title', 'genre', 'price')

admin.site.register(Artwork, ArtworkAdmin)
admin.site.register(ArtworkComment)
admin.site.register(UserLikedArtwork)
admin.site.register(Auction)
admin.site.register(Bid)
