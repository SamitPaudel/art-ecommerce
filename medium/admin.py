from django.contrib import admin

# Register your models here.
from medium.models import Medium


class MediumAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ('medium_title',)
    }
    list_display = ('medium_title','slug')

admin.site.register(Medium, MediumAdmin)