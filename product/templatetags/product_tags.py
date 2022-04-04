from django import template

register = template.Library()

def order_items_of_user(user_obj):
    if not user_obj.is_authenticated:
        return 0
        
    qs = user_obj.orders.filter(submitted=False)
    if not qs.exists():
        return 0

    order_obj = qs.get()
    total = 0
    order_itm_qs = order_obj.order_items.all()

    for order_itm in order_itm_qs:
        total += order_itm.quantity

    return total


def add(x):
    return int(x) + 10


register.filter(name="order_items_of_user", filter_func=order_items_of_user)
register.filter(name="add", filter_func=add)
