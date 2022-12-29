from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Artwork

# to get session key, generate if not available
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, artwork_id):
    artwork = Artwork.objects.get(id=artwork_id)
    try:
        # get the cart_id from the session storage
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request)
        )
    cart.save()

    # Adding items to the cart:
    try:
        cart_item = CartItem.objects.get(artwork=artwork, cart=cart)
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            artwork = artwork,
            cart = cart,
            # no need is_active as it is True by default
        )
        cart_item.save()
    return redirect('cart')


def remove_cart(request, artwork_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    artwork = get_object_or_404(Artwork, id=artwork_id)
    cart_item = CartItem.objects.get(artwork=artwork, cart=cart)
    cart_item.delete()
    return redirect('cart')


# Create your views here.
def cart(request, total=0, cart_item=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.artwork.price)
        discount = total * 0.05
        grand_total = total - discount
    except ObjectNotExist:
        pass

    context = {
        'total': total,
        'cart_items': cart_items,
        'discount': discount,
        'grand_total': grand_total
    }

    return render(request, 'cart.html', context)