from django.contrib import admin

# Register your models here.
from .models import Artist

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('artist_name',)
    }
    list_display = ('artist_name','slug')

    def display_artist_email(self, obj):
        return obj.artist_email.email

    display_artist_email.short_description = 'Artist Account'

admin.site.register(Artist, ArtistAdmin)