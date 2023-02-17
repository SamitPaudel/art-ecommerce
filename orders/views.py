import datetime

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from carts.models import CartItem
from orders.forms import OrderForm
from orders.models import Order


def payments(request):
    return render(request, 'payments.html')

def place_order(request ):
    global order_total
    current_user = request.user
    cart_items = CartItem.objects.filter(user=current_user)
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        order_total = cart_item.artwork.price
    discount = order_total * 0.05
    grand_total = order_total - discount

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.user = current_user
            data.full_name = form.cleaned_data['full_name']
            data.email = form.cleaned_data['email']
            data.phone = form.cleaned_data['phone']
            data.address = form.cleaned_data['address']
            data.order_note = form.cleaned_data['order_note']

            data.order_total = order_total
            data.discount = discount
            data.grand_total = grand_total
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            # Take current date to generate unique order no.
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%y%m%d")
            order_number = current_date + str(data.id)
            data.order_number = order_number
            data.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number=order_number)
            context = {
                'order': order,
                'cart_items': cart_items,
                'order_total': order_total,
                'discount': discount,
                'grand_total': grand_total
            }
            return render(request, 'payments.html', context)
        else:
            return redirect('checkout')
