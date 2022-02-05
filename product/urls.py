from django.urls import path
from . import views

urlpatterns = [
    path("", views.index),
    path("products/", views.shop),
    path("products/detail/", views.product_detail),
    path("checkout/", views.checkout),
]
