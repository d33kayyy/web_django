from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.shortcuts import render

from .models import Item
from .forms import ItemForm


class HomePageView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'new_items'

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by('-pub_date').all()


class ItemView(generic.DetailView):
    model = Item
    template_name = 'item/detail.html'


class IndexView(generic.ListView):
    template_name = 'item/index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by('-pub_date').all()

class CreateItem(LoginRequiredMixin, generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add.html'

def cook(request):
    return render(template_name='cook.html', request=request)