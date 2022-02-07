from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import login, authenticate, logout



User = get_user_model()


class HomePage(ListView):
    """
    HOME PAGE
    """
    template_name = "product/index.html"

    def get_queryset(self):
        pass

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

    def get_queryset(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def shop(request):

    return render(request, "product/shop.html")


class ProductDetailPage(DetailView):
    """
    PRODUCT PAGE
    """
    template_name = "product/product_detail.html"
    lookup_url_kwarg = "product_id"

    # def get_queryset(self):
    #     pass

    def get_object(self):
        pass

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


def product_detail(request):

    return render(request, "product/product_detail.html")


def checkout(request):

    return render(request, "product/checkout.html")
