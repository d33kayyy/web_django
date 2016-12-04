from django.forms import formset_factory
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages

from order.models import ItemOrder, Order
from item.models import Item

from .utils import get_session, CART_SESSION, INFO_SESSION
from .forms import ItemOrderForm, ItemForm, InformationForm


class CartView(FormView):
    '''
    Display Cart page and handle cart update
    '''

    template_name = 'cart/cart.html'
    form_class = formset_factory(ItemOrderForm, extra=0)
    success_url = reverse_lazy('cart:cart')
    success_message = _(u'Cart updated!')

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        context['cart'] = get_session(self.request, CART_SESSION)
        return context

    def get_initial(self):
        cart = get_session(self.request, CART_SESSION)
        initial = [{'item_id': k, 'quantity': v} for k, v in cart.items()]

        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            if 'checkout' in request.POST:
                # if the button clicked is 'checkout', redirect to info page
                self.success_url = reverse('cart:info')
                self.success_message = None

            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        cart = get_session(self.request, CART_SESSION)
        formset = form

        # update cart
        for f in formset:
            item_id = f.cleaned_data['item_id']
            quantity = f.cleaned_data['quantity']
            cart.update({str(item_id): quantity})

        # self.request.session[CART_SESSION] = cart
        self.request.session.modified = True
        if self.success_message:
            messages.success(self.request, self.success_message)

        return super(CartView, self).form_valid(form)


class AddItemToCart(FormView):
    '''
    Add new item to cart
    '''
    form_class = ItemOrderForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        item_id = form.cleaned_data['item_id']
        quantity = 1

        cart = get_session(self.request, CART_SESSION)
        exist = cart.get(str(item_id))

        if exist:
            cart[str(item_id)] += quantity
        else:
            cart[str(item_id)] = quantity

        self.request.session[CART_SESSION] = cart
        self.request.session.modified = True

        item = Item.objects.get(id=item_id)
        success_message = _(u'{} added to cart!'.format(item.name))
        messages.success(self.request, success_message)

        return HttpResponseRedirect(reverse('cart:cart'))


class RemoveItemFromCart(FormView):
    '''
    Delete item from cart
    '''
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        cart = get_session(self.request, CART_SESSION)
        item_id = form.cleaned_data['item_id']

        # remove item from cart session
        if str(item_id) in cart.keys():
            del cart[str(item_id)]

        self.request.session.modified = True

        item = Item.objects.get(id=item_id)
        success_message = _(u'{} removed from cart!'.format(item.name))
        messages.success(self.request, success_message)

        return HttpResponseRedirect(reverse('cart:cart'))


def information(request):
    '''
    Information form when ordering
    :param request:
    :return:
    '''

    cart = get_session(request, CART_SESSION)
    if not cart:
        return HttpResponseRedirect(reverse('cart:cart'))

    if request.user.is_authenticated():
        profile = request.user.profile
        form = InformationForm(initial={'name': profile.name,
                                        'address': profile.address,
                                        'phone': profile.phone,
                                        'email': profile.email, })
    else:
        form = InformationForm

    if request.method == 'POST':
        form = InformationForm(request.POST)

        if form.is_valid():

            # push data into info session
            info = get_session(request, INFO_SESSION)
            for k, v in form.cleaned_data.items():
                info[str(k)] = v

            request.session[INFO_SESSION] = info
            request.session.modified = True
            return HttpResponseRedirect(reverse('cart:confirm'))

    return render(request, 'cart/information.html', {'form': form})


def confirmation(request):
    '''
    Confirmation page and create new order if transaction succeed
    :param request:
    :return:
    '''
    cart = get_session(request, CART_SESSION)
    info = get_session(request, INFO_SESSION)

    if not info:
        return HttpResponseRedirect(reverse('cart:info'))

    if request.method == 'POST':
        if request.user.is_authenticated():
            profile = request.user.profile
        else:
            profile = None

        # Create order
        order = Order.objects.create(userprofile=profile,
                                     receiver=info['name'],
                                     note=info['note'],
                                     phone=info['phone'],
                                     address=info['address'],
                                     email=info['email'],
                                     city=info['city'],
                                     district=info['district'], )
        # Create item order
        for item_id, quantity in cart.items():
            item = Item.objects.get(id=item_id)
            item_order = ItemOrder.objects.create(order=order, item=item, quantity=quantity)

        # Clear the session
        cart.clear()
        info.clear()
        request.session.modified = True

        return HttpResponseRedirect(reverse('order:detail', args=(str(order.id),)))

    return render(request, 'cart/confirm.html', {'cart': cart, 'info': info})
