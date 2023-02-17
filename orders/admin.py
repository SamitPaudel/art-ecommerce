from django.contrib import admin

# Register your models here.
from orders.models import Order, OrderArtwork, Payment

admin.site.register(Order)
admin.site.register(OrderArtwork)
admin.site.register(Payment)
