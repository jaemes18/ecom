from .cart import Cart
from django.contrib.auth.models import User

def cart(request):
    user = request.user
    return {'cart': Cart(request)}