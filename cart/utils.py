CART_SESSION = 'cart'
INFO_SESSION = 'info'


def get_session(request, session_name):
    """
    Get session or create an empty session if not exist.
    """
    cart = request.session.get(session_name, {})
    if cart is None:
        request.session[session_name] = {}
        cart = request.session[session_name]
    return cart
