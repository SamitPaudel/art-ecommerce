from django.contrib import admin

# Register your models here.
from .models import Artist

class ArtistAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('artist_name',)
    }
    list_display = ('artist_name','slug')

admin.site.register(Artist, ArtistAdmin)