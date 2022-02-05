from django.shortcuts import render


def index(request):

    return render(request, "product/index.html")


def shop(request):

    return render(request, "product/shop.html")


def product_detail(request):

    return render(request, "product/product_detail.html")


def checkout(request):

    return render(request, "product/checkout.html")
