from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import messages
from ecom.models import Product, Profile
import datetime


def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        items = OrderItem.objects.filter(order=pk)
        if request.method == 'POST':
            status = request.POST['shipping_status']
            num = request.POST['num']
            if status == 'true':
                order = Order.objects.filter(id=pk)
                now = datetime.datetime.now()
                order.update(shipped=True, date_shipped=now)
            else:
                order = Order.objects.filter(id=pk)
                order.update(shipped=False)
            messages.success(request, "Shipping Status Updated ")
            return redirect('ecom:home')
        return render(request, 'payment/orders.html', {'order': order, 'items': items})


def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=True)
        if request.method == 'POST':
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=False)

            messages.success(request, "Shipping Status Updated ")
            return redirect('ecom:home')
        return render(request, 'payment/shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('ecom:home')

def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders = Order.objects.filter(shipped=False)
        if request.method == 'POST':
            status = request.POST['shipping_status']
            num = request.POST['num']
            order = Order.objects.filter(id=num)

            now = datetime.datetime.now()
            order.update(shipped=True)

            messages.success(request, "Shipping Status Updated ")
            return redirect('ecom:home')
        return render(request, 'payment/not_shipped_dash.html', {'orders': orders})
    else:
        messages.success(request, 'Access Denied')
        return redirect('ecomt:home')

def process_order(request):
    if request.POST:
        payment_form = PaymentForm(request.POST or None)
        my_shipping  = request.session.get('my_shipping')
        shipping_address = f"{my_shipping['shipping_address1']}\n,{my_shipping['shipping_address2']}\n,{my_shipping['shipping_city']}\n,{my_shipping['shipping_state']}\n,{my_shipping['shipping_country']}\n,{ my_shipping['shipping_zip_code']}"
        cart = Cart(request)
        carty = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        user = request.user
        full_name= my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
        amount_paid=totals
        shipping_address = f"{my_shipping['shipping_address1']}\n,{my_shipping['shipping_address2']}\n,{my_shipping['shipping_city']}\n,{my_shipping['shipping_state']}\n,{my_shipping['shipping_country']}\n,{my_shipping['shipping_zip_code']}"
        if request.user.is_authenticated:
            user = request.user
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in carty():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key,value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id,product_id=product_id,user_id=user.id,quantity=value,price=price)
                        create_order_item.save()
                for key in list(request.session.keys()):
                    if key == 'session_key':
                        del request.session[key]

                current_user = Profile.objects.filter(user__id=request.user.id)
                current_user.update(old_cart="")

            messages.success(request, "Order Placed")
            return redirect('ecom:home')
        else:
            create_order = Order(user=user, full_name=full_name, email=email, shipping_address=shipping_address, amount_paid=amount_paid)
            create_order.save()
            order_id = create_order.pk
            for product in carty():
                product_id = product.id
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for key, value in quantities().items():
                    if int(key) == product.id:
                        create_order_item = OrderItem(order_id=order_id, product_id=product_id, user_id=user.id,
                                                      quantity=value, price=price)
                        create_order_item.save()
                for key in list(request.session.keys()):
                    if key == 'session_key':
                        del request.session[key]
            messages.success(request, 'Order Placed')
            return redirect('ecom:home')
        return redirect('ecom:home')
    else:
        messages.success((request, 'Access Denied'))
        return redirect('ecom:home')
def billing_info(request):
    if request.POST:
        cart = Cart(request)
        carty = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping
        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {'cart_products': carty, 'quantities': quantities, 'totals': totals,
                           'shipping_info': request.POST, 'billing_form': billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {'cart_products': carty, 'quantities': quantities, 'totals': totals,
                           'shipping_info': request.POST, 'billing_form': billing_form})
        shipping_info = request.POST
        return render(request, 'payment/billing_info.html',
                      {'cart_products': carty, 'quantities': quantities, 'totals': totals,
                       'shipping_form': shipping_info})
    else:
        messages.success(request, "Access Denied! ")
        return redirect('ecom:home')

def checkout(request):
    cart = Cart(request)
    carty = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html',
                      {'cart_products': carty, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html',
                  {'cart_products': carty, 'quantities': quantities, 'totals': totals, 'shipping_form': shipping_form})

def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

# Create your views here.