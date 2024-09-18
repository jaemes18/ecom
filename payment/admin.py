from django.contrib import admin
from .models import ShippingAddress, Order,OrderItem
from django.contrib.auth.models import User



admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)

class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    model = Order
    inlines = [OrderItemInline]
    fields = ['user', 'full_name','shipping_address','amount_paid', 'email', 'order_date','shipped', 'date_shipped']
    readonly_fields = ["order_date"]


admin.site.unregister(Order)

admin.site.register(Order, OrderAdmin)
# Register your models here.
