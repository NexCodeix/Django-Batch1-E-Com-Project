from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), ),
    path("products/", views.ShopPage.as_view(), ),
    path("products/detail/", views.ProductDetailPage.as_view(), ),
    path("checkout/", views.checkout),
]
