from django.contrib import admin
from .models import Order, OrderItem, Item, Profile, ShippingAddress


admin.site.register(Profile)
admin.site.register(ShippingAddress)
admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order)
