from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(ShippingAddress)
