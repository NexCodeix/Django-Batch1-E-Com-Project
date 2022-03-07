from django.http import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import login, authenticate, logout
from .models import Product, OrderItem, Order
from django.db.models import Q

from django.core.exceptions import PermissionDenied

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
    paginate_by = 2

    def filter_by_category(self, qs):
        pass

    def get_products(self):
        starting_price = self.request.GET.get("strtp")
        end_price = self.request.GET.get("endp")

        # if (starting_price) and (not end_price):
        #     pass

        # if (end_price) and (not starting_price):
        #     pass

        if starting_price and end_price:
            return self.filter_qs_by_price(starting_price, end_price)

        qs = Product.objects.all()
        return qs

    def filter_qs_by_price(self, starting_price, end_price):
        try:
            starting_price = float(starting_price)
            end_price = float(end_price)
        except ValueError:
            return Product.objects.all()

        qs = Product.objects.filter(Q(price__gte=starting_price) & Q(price__lte=end_price))

        return qs

    def get_queryset(self):
        products = self.get_products()
        return products

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

    def get_filtered_qs(self, slug):
        qs = Product.objects.filter(slug=slug)
        if not qs.exists():
            raise Http404
        self.queryset = qs
        return qs

    def get_product(self):
        slug = self.kwargs.get(self.lookup_url_kwarg)
        product = self.get_filtered_qs(slug).get()
        self.object = product
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        tags = product.tags.all()

        product_qs = Product.objects.none()  # []
        for tag in tags:
            products = tag.product_set.all()
            print("Tag Products ", products)
            product_qs |= products  # append\

        if not product_qs.exists():
            main_qs = Product.objects.all()[:4]
        else:
            if product_qs.count() < 4:
                qs1 = Product.objects.all()[:4 - product_qs.count()]
                print("SELF", self.queryset)
                main_qs = self.queryset | qs1
            else:
                main_qs = product_qs

            main_qs = main_qs.distinct()
        print(main_qs)
        # print("Tags -> ", tags)
        # print("Queryset ", product_qs)
        context["similar_products"] = main_qs
        return context


def product_detail(request):

    return render(request, "product/product_detail.html")


def checkout(request):

    return render(request, "product/checkout.html")


def order_item(request, product_slug):
    if not request.user.is_authenticated:
        raise PermissionDenied("")
    if request.method != "POST":
        raise Http404("User POST METHOD")
    product_obj = get_object_or_404(Product, slug=product_slug)
    user = request.user
    order_qs = user.orders.filter(submitted=False)
    if order_qs.exists():
        print("Got an Existing Order")
        order_obj = order_qs.get()
    else:
        print("Created a New Order")
        order_obj = Order.objects.create(user=user)

    product_qs = order_obj.products.filter(id=product_obj.id)
    if product_qs.exists():
        print("Found Product in this Order")
        order_item_obj = order_obj.order_items.get(product=product_obj)
        order_item_obj.quantity += 1
        order_item_obj.save()

    else:
        print("Adding Products to the order")
        order_obj.products.add(product_obj)
        order_obj.save()

    print("Product Added \n \n")


    return JsonResponse("Product Added", safe=False)
