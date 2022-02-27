from django.urls import path
from . import views


urlpatterns = [
    path("product/<product_slug>/reviews/", views.ReviewListCreateAPIView.as_view(), ),
]
