from django.shortcuts import render, get_object_or_404
from ecom.models import Product
from django.http import JsonResponse
from .cart import Cart
from django.urls import reverse
#url = reverse('cart_add')

def cart_summary(request):
    cart = Cart(request)
    carty = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    cart_quantity = cart.__len__()  # Get the cart length
    return render(request, 'cart/cart_summary.html', {
        'cart_products': carty,
        'quantities': quantities,
        'totals': totals,
        'cart_quantity': cart_quantity  # Pass it to the template
    })
def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty= int(request.POST.get('product_qty'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'Qty': cart_quantity})
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        cart.update(product=product_id,quantity= product_qty)
        response = JsonResponse({'qty':product_qty})
        return response
        #return redirect('cart/cart_summary.html)

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        cart.delete(product=product_id)
        response = JsonResponse({'product': product_id})
        return response