from django import template
from item.models import Item

from ..utils import get_cart
register = template.Library()

@register.simple_tag
def get_item(item_id):
    try:
        item = Item.objects.get(id=item_id)
    except Exception as e:
        return False
    return item

@register.simple_tag(takes_context=True)
def get_subtotal(context, item_id, quantity):
    try:
        cart = get_cart(context['request'])
        item = Item.objects.get(id=item_id)
        total_price = item.price * cart[str(item_id)]
    except Exception:
        total_price = 0
    return total_price


