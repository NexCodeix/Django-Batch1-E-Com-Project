import secrets
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

User = get_user_model()


class Product(models.Model):
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(unique=True)

    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == ""):
            self.slug = slugify(self.name) + str(secrets.token_hex(6))

        return super().save(*args, **kwargs)


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ordered")
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        quantity = self.quantity
        if quantity and (quantity < 1):
            raise ValueError("Quantity cannot be 0")

        return super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="order_items")
    products = models.ManyToManyField(Product, through=OrderItem)
    transaction_numb = models.CharField(max_length=500)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        transaction_numb = self.transaction_numb
        if (transaction_numb is None) or (transaction_numb == ""):
            self.transaction_numb = str(secrets.token_hex(50))

        return super().save(*args, **kwargs)
