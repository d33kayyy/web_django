from django.forms import Form, formset_factory
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import FormView, FormMixin

from item.models import Item
from .utils import get_cart, CART_SESSION
from .forms import ItemOrderForm, ItemForm


class CartView(FormView):
    template_name = 'order/cart.html'
    form_class = formset_factory(ItemOrderForm, extra=0)
    success_url = reverse_lazy('order:cart')

    def get_initial(self):
        cart = get_cart(self.request)
        initial = [{'item_id': k, 'quantity': v} for k, v in cart.items()]

        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        print('in CartView')
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        cart = get_cart(self.request)
        formset = form
        for f in formset:
            item_id = f.cleaned_data['item_id']
            quantity = f.cleaned_data['quantity']
            cart.update({str(item_id): quantity})

        # self.request.session[CART_SESSION] = cart
        self.request.session.modified = True

        return HttpResponseRedirect(self.get_success_url())


def index(request):
    cart = get_cart(request)
    initial = [{'item_id': k, 'quantity': v} for k, v in cart.items()]

    return render(context={'cart': initial}, template_name='order/cart.html', request=request)


class AddItemToCart(FormView):
    form_class = ItemOrderForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        item_id = form.cleaned_data['item_id']
        quantity = 1

        cart = get_cart(self.request)
        exist = cart.get(str(item_id))

        if exist:
            cart[str(item_id)] += quantity
        else:
            cart[str(item_id)] = quantity

        self.request.session[CART_SESSION] = cart
        self.request.session.modified = True

        return HttpResponseRedirect(reverse('order:cart'))


class RemoveItemFromCart(FormView):
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        cart = get_cart(self.request)
        item_id = form.cleaned_data['item_id']
        if str(item_id) in cart.keys():
            del cart[str(item_id)]

        self.request.session.modified = True

        return HttpResponseRedirect(reverse('order:cart'))
