from django import template

from web_django.settings import CART_SESSION
from cart.utils import get_session
from item.models import Item

register = template.Library()

SHIPPING = 0


@register.simple_tag
def get_item(item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Exception:
        return False
    return item


@register.simple_tag(takes_context=True)
def get_subtotal(context, item_id):
    try:
        cart = get_session(context['request'], CART_SESSION)
        item = Item.objects.get(id=item_id)
        total_price = item.price * cart[str(item_id)]
    except Exception:
        total_price = 0
    return total_price


@register.simple_tag(takes_context=True)
def get_total_price(context):
    try:
        total_price = 0
        cart = get_session(context['request'], CART_SESSION)
        for item_id, quantity in cart.items():
            item = Item.objects.get(id=item_id)
            total_price += (item.price * int(quantity))
    except Exception:
        total_price = 0
    return total_price


@register.simple_tag(takes_context=True)
def get_total_with_ship(context):
    try:
        total = get_total_price(context)
        total += SHIPPING
    except Exception:
        total = 0
    return total


@register.simple_tag
def get_shipping():
    return SHIPPING
