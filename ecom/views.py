from django.shortcuts import render, redirect
from django.http import HttpResponse
from ecom.models import Product, Category, Profile
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForms
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django.http import HttpResponseBadRequest
from django.core.exceptions import ValidationError
import json


def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user=request.user)
            shipping_user = ShippingAddress.objects.get(user=request.user)
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found.")

            return redirect('ecom:home')
        except ShippingAddress.DoesNotExist:
            messages.error(request, "Shipping Address not found.")
            return redirect('ecom:home')
        form = UserInfoForms(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, "Your Info Has Been Updated!")
            return redirect('ecom:home')
        return render(request, 'ecom/update_info.html', {"form": form, "shipping_form": shipping_form})
    else:
        messages.error(request, "You need to be logged in to update your info.")

        return redirect('ecom:home')


def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'ecom/category_summary.html', {'categories': categories})



def category(request, foo):
    foo = foo.replace(" ", "-")
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'ecom/category.html', {'products': products, 'category': category})
    except Category.DoesNotExist:
        messages.error(request, "THAT CATEGORY DOESN'T EXIST")
        return redirect("ecom:home")


def search(request):
    if request.method == 'POST':
        searched = request.POST.get('searched', '')
        searched_products = Product.objects.filter(name__icontains=searched)
        if not searched_products:
            messages.info(request, 'PRODUCT NOT FOUND')
        return render(request, 'ecom/search.html', {'searched': searched_products})
    return render(request, 'ecom/search.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "Logged Out Successfully")
    return redirect('ecom:home')

def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)
        if user_form.is_valid():
            user_form.save()
            login(request, current_user)
            messages.success(request, "User Has Been Updated!")
            return redirect('ecom:home')
        return render(request, 'ecom/update_user.html', {"user_form": user_form})
    else:
        messages.error(request, "You need to be logged in to update user info.")
        return redirect('ecom:home')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                current_user = Profile.objects.get(user=request.user)
                saved_cart = current_user.old_cart
                if saved_cart:
                    converted_cart = json.loads(saved_cart)
                    cart = Cart(request)
                    for key, value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)
            except Profile.DoesNotExist:
                messages.error(request, "Profile not found.")
            messages.success(request, "LOGGED IN SUCCESSFULLY")
            return redirect('ecom:home')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('ecom:login')
    return render(request, 'ecom/login.html', {})



def category_summary(request):
    categories = Category.objects.all()
    return render(request, 'ecom/category_summary.html', {'categories': categories})




def product_detail(request, pk):
    try:
        products = Product.objects.get(id=pk)
    except Product.DoesNotExist:
        messages.error(request, "Product not found.")
        return redirect('ecom:home')
    return render(request, 'ecom/product.html', {'products': products})


def say_hello(request):
        products = Product.objects.all()
        return render(request, 'ecom/home.html', {'products':products})

def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password changed successfully.')
                return redirect('ecom:home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
        else:
            form = ChangePasswordForm(current_user)
        return render(request, 'ecom/update_password.html', {'form': form})
    else:
        return redirect('ecom:login')


def about(request):
    return render(request, 'ecom/about.html', {})


def register_user(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome! {username} You Have Registered")
                return redirect('ecom:update_info')
        messages.error(request, "There was a problem with your registration.")
    return render(request, 'ecom/register.html', {"form": form})
