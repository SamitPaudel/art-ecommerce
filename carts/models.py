from django.db import models

# Create your models here.
from store.models import Artwork



class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.artwork


