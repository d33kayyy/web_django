from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views import generic
from django.shortcuts import render

from .models import Item
from .forms import ItemForm


class HomePageView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'list_items'

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


class CreateItem(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add_edit.html'
    success_message = 'Item successfully created'

    def form_valid(self, form):
        item = form.save(commit=False)
        item.chef = self.request.user
        return super(CreateItem, self).form_valid(form)


class EditItem(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add_edit.html'
    success_message = 'Changes have been saved.'


def cook(request):
    return render(template_name='cook.html', request=request)
