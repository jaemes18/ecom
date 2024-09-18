from django.contrib import admin
from django.contrib import admin
from .models import Category
from .models import Customer
from .models import Product
from .models import Order, Profile
from django.contrib.auth.models import User



admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Profile)
# Register your models here.

class ProfileInLine(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username', 'first_name', 'last_name', 'email']
    inlines = [ProfileInLine]


admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register your models here.
