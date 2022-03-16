from django.contrib import admin
from .models import Product, ProductImages, Order, OrderItem, Tag, BillingAddress
from .models import Product, ProductImages, Order, OrderItem, Tag,Subscribe

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImages)
admin.site.register(Tag)
admin.site.register(BillingAddress)
admin.site.register(Subscribe)
