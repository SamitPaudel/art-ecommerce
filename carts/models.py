from django.db import models

# Create your models here.
from accounts.models import Account
from store.models import Artwork



class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

    def clear_cart(self):
        self.cartitem_set.all().delete()


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.full_name} - {self.artwork.artwork_title}"



