from django.contrib import admin

# Register your models here.
from genre.models import Genre

class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('title',)
    }
    list_display = ('title','slug')

admin.site.register(Genre, GenreAdmin)