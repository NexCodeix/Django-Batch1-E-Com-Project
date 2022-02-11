from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import login, authenticate, logout
from .models import Product, OrderItem, Order


User = get_user_model()


class HomePage(ListView):
    """
    HOME PAGE
    """
    context_object_name = "products"
    template_name = "product/index.html"

    def get_queryset(self):
        qs = Product.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(context)
        return context


def index(request):
    context = {

    }
    return render(request, "product/index.html", context)


class ShopPage(ListView):
    """
    Shop PAGE
    """
    template_name = "product/shop.html"
    context_object_name = "products"

    def get_queryset(self):
        qs = Product.objects.all()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def shop(request):

    return render(request, "product/shop.html")


class ProductDetailPage(DetailView):
    """
    PRODUCT PAGE
    """
    context_object_name = "product"
    template_name = "product/product_detail.html"
    lookup_url_kwarg = "product_slug"

    # def get_queryset(self):
    #     pass

    def get_object(self):
        return self.get_product()

    def get_product(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        product = get_object_or_404(Product, slug=slug)
        self.object = product
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        tags = product.tags.all()

        qs = Product.objects.none()  # []
        for tag in tags:
            products = tag.product_set.all()
            qs |= products.distinct()  # append\
            qs = qs.distinct()

        if not qs.exists():
            qs = Product.objects.all()[:5]

        print("Tags -> ", tags)
        print("Queryset ", qs)
        context["similar_products"] = qs.distinct()
        return context


def product_detail(request):

    return render(request, "product/product_detail.html")


def checkout(request):

    return render(request, "product/checkout.html")
