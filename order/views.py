from django.forms import Form, formset_factory
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DetailView
from django.views.generic.edit import FormView, FormMixin

from .models import ItemOrder, Order
from item.models import Item

from .utils import get_session, CART_SESSION, INFO_SESSION
from .forms import ItemOrderForm, ItemForm, InformationForm


class CartView(FormView):
    template_name = 'order/cart.html'
    form_class = formset_factory(ItemOrderForm, extra=0)
    success_url = reverse_lazy('order:cart')

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
                self.success_url = reverse('order:info')

            return self.form_valid(form)
        else:
            print(form.errors)
            return self.form_invalid(form)

    def form_valid(self, form):
        cart = get_session(self.request, CART_SESSION)
        formset = form
        for f in formset:
            item_id = f.cleaned_data['item_id']
            quantity = f.cleaned_data['quantity']
            cart.update({str(item_id): quantity})

        # self.request.session[CART_SESSION] = cart
        self.request.session.modified = True

        return HttpResponseRedirect(self.get_success_url())


class AddItemToCart(FormView):
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

        return HttpResponseRedirect(reverse('order:cart'))


class RemoveItemFromCart(FormView):
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        cart = get_session(self.request, CART_SESSION)
        item_id = form.cleaned_data['item_id']
        if str(item_id) in cart.keys():
            del cart[str(item_id)]

        self.request.session.modified = True

        return HttpResponseRedirect(reverse('order:cart'))


def information(request):
    cart = get_session(request, CART_SESSION)
    if not cart:
        return HttpResponseRedirect(reverse('order:cart'))

    if request.user.is_authenticated():
        profile = request.user.profile
        form = InformationForm(initial={'name': profile.name,
                                        'address': profile.address,
                                        'phone': profile.phone,
                                        'email': profile.email,})
    else:
        form = InformationForm

    if request.method == 'POST':
        form = InformationForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)

            info = get_session(request, INFO_SESSION)
            for k, v in form.cleaned_data.items():
                info[str(k)] = v

            request.session[INFO_SESSION] = info
            request.session.modified = True
            return HttpResponseRedirect(reverse('order:confirm'))

    return render(request, 'order/information.html', {'form': form})


def confirmation(request):
    cart = get_session(request, CART_SESSION)
    info = get_session(request, INFO_SESSION)

    if not info:
        return HttpResponseRedirect(reverse('order:info'))

    if request.method == 'POST':
        if request.user.is_authenticated():
            customer = request.user.profile
        else:
            customer = None

        order = Order.objects.create(customer=customer,
                                     receiver=info['name'],
                                     note=info['note'],
                                     phone=info['phone'],
                                     address=info['address'],
                                     # email=info['email'],
                                     city=info['city'],
                                     district=info['district'], )

        for item_id, quantity in cart.items():
            item = Item.objects.get(id=item_id)
            item_order = ItemOrder.objects.create(order=order, item=item, quantity=quantity)

        cart.clear()
        info.clear()
        request.session.modified = True
        return HttpResponseRedirect(reverse('order:detail', args=(str(order.id),)))

    return render(request, 'order/confirm.html', {'cart': cart, 'info': info})


class OrderView(DetailView):
    model = Order
    template_name = 'order/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderView, self).get_context_data(**kwargs)
        context['items'] = ItemOrder.objects.filter(order=self.object)
        return context
