from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView

from .models import ItemOrder, Order


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)
        context['items'] = ItemOrder.objects.filter(order=self.object)
        return context


class ListOrdersView(LoginRequiredMixin, ListView):
    template_name = 'order/history.html'

    def get_queryset(self):
        return Order.objects.order_by('-order_date').filter(customer=self.request.user.profile)

