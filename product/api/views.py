from ..models import Review, Product
from .serializers import ReviewSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.exceptions import MultipleObjectsReturned
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


def get_object_or_rest_404(klass, **kwargs):
    qs = klass.objects.filter(**kwargs)
    if qs.exists():
        try:
            return qs.get()
        except MultipleObjectsReturned as e:
            raise ValidationError(e)

    raise ValidationError('Object does not exist.')


class ReviewListCreateAPIView(ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    lookup_url_kwarg = "product_slug"

    def perform_create(self, serializer):
        product = self.get_product()
        try:
            serializer.save(user=self.request.user, product=product)
        except IntegrityError as e:
            raise ValidationError(e)

    def get_queryset(self):
        product = self.get_product()
        qs = product.reviews.all()
        return qs

    def get_product(self):
        product_slug = self.kwargs.get(self.lookup_url_kwarg)
        return get_object_or_rest_404(Product, slug=product_slug)

