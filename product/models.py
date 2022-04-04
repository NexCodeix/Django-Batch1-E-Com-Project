import uuid
import secrets
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.core.exceptions import ValidationError


User = get_user_model()

def uuid_without_dash():
    return uuid.uuid4().hex


def validate_rating(value):
    value = int(value)
    if value > 5:
        raise ValidationError("Rating cannot be more than 5")

    return value


class Product(models.Model):
    PRODUCT_CATEGORY = (
        ("dress", "dress"),
        ("bag", "bag"),
        ("shirt", "shirt"),
        ("cloth", "cloth"),
        ("jacket", "jacket"),
    )
    name = models.CharField(max_length=500)
    description = models.TextField()
    price = models.FloatField()
    slug = models.SlugField(unique=True)
    tags = models.ManyToManyField("Tag")
    files = models.FileField(upload_to="documents", null=True, blank=True)
    category = models.CharField(max_length=100, choices=PRODUCT_CATEGORY)
    image = models.ImageField(upload_to="products", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        slug = self.slug
        if (slug is None) or (slug == ""):
            self.slug = slugify(self.name) + str(secrets.token_hex(6))

        return super().save(*args, **kwargs)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product_images", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, editable=False, default=uuid_without_dash)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews_given")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    text = models.TextField()
    rating = models.PositiveSmallIntegerField(validators=[validate_rating])
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["user", "product"]

    def __str__(self):
        return f"{self.user} reviewed {self.product}"


class OrderItem(models.Model):
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ordered")
    quantity = models.PositiveIntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def all_info_to_text(self):
        return f"${self.product.price} * {self.quantity} = ${self.get_total}"

    @property
    def get_total(self):
        return self.product.price * self.quantity

    def save(self, *args, **kwargs):
        quantity = self.quantity
        if quantity and (quantity < 1):
            raise ValueError("Quantity cannot be 0")

        return super().save(*args, **kwargs)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    products = models.ManyToManyField(Product, through=OrderItem)
    transaction_numb = models.CharField(max_length=500)
    submitted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        transaction_numb = self.transaction_numb
        if (transaction_numb is None) or (transaction_numb == ""):
            self.transaction_numb = str(secrets.token_hex(50))

        return super().save(*args, **kwargs)

    def get_all_items(self):
        qs = self.order_items.all()
        return qs

    def total_bill(self):
        items = self.get_all_items()
        total = 0
        for i in items:
            total += int(i.get_total)

        return total

class BillingAddress(models.Model):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid_without_dash, editable=False)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="billing")
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    email = models.EmailField()
    mobile = models.CharField(max_length=300)
    address = models.TextField()
    city = models.CharField(max_length=300)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.first_name} {self.last_name} order"
    
    
class Subscribe(models.Model):
    name = models.CharField(max_length=100)
    email =models.CharField( max_length=50)
    date_created=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name 
