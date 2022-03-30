from django.shortcuts import redirect
from django.contrib import messages
from django.contrib import admin
from .forms import ProductAdminForm, ProductAdminAddForm
from .models import Product, ProductImages, Order, OrderItem, Tag, BillingAddress
from .models import Product, ProductImages, Order, OrderItem, Tag,Subscribe

from django.contrib.auth.admin import UserAdmin


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "slug")
    add_form = ProductAdminAddForm
    form = ProductAdminForm

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def response_add(self, request, obj, post_url_continue=None):
        # redirect url after adding
        messages.success(request, "Added")
        return redirect(f'/admin/product/product/{obj.id}/change/')

    def response_change(self, request, obj):
        # redirect url after editing
        messages.success(request, "Edited")
        return redirect('/admin/product/product/')


admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImages)
admin.site.register(Tag)
admin.site.register(BillingAddress)
admin.site.register(Subscribe)
