CART_SESSION = 'cart'
INFO_SESSION = 'info'


def get_session(request, session_name):
    """
    Get cart session or create an empty cart if not exist.
    """
    cart = request.session.get(session_name, {})
    if cart is None:
        request.session[session_name] = {}
        cart = request.session[session_name]
    return cart
