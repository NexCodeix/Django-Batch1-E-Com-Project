from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomePage.as_view(), ),
    path("shop/", views.ShopPage.as_view(), name="shop"),
    path("products/detail/<product_slug>/", views.ProductDetailPage.as_view(), name="product_detail"),
    # path("checkout/", views.CheckoutView.as_view()),
    path("subscribe/", views.subscribe,name="subscribe"),

    path("order/item/<product_slug>/", views.order_item, name="Order-Item")
]
