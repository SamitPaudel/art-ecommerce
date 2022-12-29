from django.contrib import admin

# Register your models here.
from medium.models import Medium
from store.models import Artwork


class ArtworkAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('artwork_title',)
    }
    list_display = ('artwork_title', 'artist_name', 'medium_title', 'genre', 'price')

admin.site.register(Artwork, ArtworkAdmin)