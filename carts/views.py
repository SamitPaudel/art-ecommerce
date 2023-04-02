from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from carts.models import Cart, CartItem
from store.models import Artwork


# to get session key, generate if not available
global cart_item
User = get_user_model()
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

@login_required
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
            user=request.user,
            artwork = artwork,
            cart = cart,
        )
        cart_item.save()
    messages.success(request, f"{artwork.artwork_title} added to cart!")
    return redirect('home')

@login_required
def remove_cart(request, artwork_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    artwork = get_object_or_404(Artwork, id=artwork_id)
    cart_item = CartItem.objects.get(artwork=artwork, cart=cart)
    cart_item.delete()
    return redirect('cart')


# Create your views here.
def cart(request, total=0, cart_item=None):
    cart_items = None
    discount = None
    grand_total = None

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += int(cart_item.artwork.price)
        discount = int(total * 0.05)
        grand_total = int(total - discount)
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_items': cart_items,
        'discount': discount,
        'grand_total': grand_total
    }

    return render(request, 'cart.html', context)

@login_required(login_url='login')
def checkout(request, total=0, cart_item=None):
    user = request.user
    try:
        total = 0
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.artwork.price)
        discount = total * 0.05
        grand_total = total - discount
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'cart_items': cart_items,
        'discount': discount,
        'grand_total': grand_total,
        'user': user,
    }
    return render(request, 'checkout.html', context)


def finalize_checkout(request):
    if request.method == 'POST':
        cart = Cart.objects.latest('date_added')
        print(f"Cart: {cart}")
        # Get the items in the cart
        cart_items = cart.cartitem_set.all()
        if cart_items:
            print("If block entered")
            for item in cart_items:
                artwork = Artwork.objects.get(id=item.artwork_id)
                print(artwork.artwork_title)
                artwork.isAvailable = False
                artwork.save()
                item.delete()
            request.session['cart_items'] = []
        return redirect('home')