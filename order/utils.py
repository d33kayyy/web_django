from .models import Order


CART_SESSION = 'cart'


def get_cart(request):
    """
    Get cart session or create an empty cart if not exist.
    """
    cart = request.session.get(CART_SESSION, {})
    if cart is None:
        request.session[CART_SESSION] = {}
        cart = request.session[CART_SESSION]
    return cart
