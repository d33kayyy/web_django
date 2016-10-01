from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.urls import reverse
from django.views import generic
from django.shortcuts import render, get_object_or_404

from silisili import settings
from .models import Item, Images
from .forms import ItemForm, ImageForm


class HomePageView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by('-pub_date').all()


class IndexView(generic.ListView):
    template_name = 'item/index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by('-pub_date').all()


class ItemDetailView(generic.DetailView):
    model = Item
    template_name = 'item/detail.html'


class CreateItemView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add_edit.html'
    success_message = 'Item successfully created'

    def form_valid(self, form):
        item = form.save(commit=False)
        item.chef = self.request.user
        return super(CreateItemView, self).form_valid(form)


class EditItemView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add_edit.html'
    success_message = 'Changes have been saved.'


def cook(request):
    return render(template_name='cook.html', request=request)


@login_required
def create_item(request):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3, max_num=3)

    if request.method == 'POST':

        item_form = ItemForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if item_form.is_valid() and formset.is_valid():

            item = item_form.save(commit=False)
            item.chef = request.user
            item.save()

            for form in formset.cleaned_data:
                if form and form['image']:
                    image = form['image']
                    photo = Images(item=item, image=image)
                    photo.save()

            return HttpResponseRedirect(reverse('item:detail', args=(item.id,)))

    else:
        item_form = ItemForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'item/add_edit.html', {'item_form': item_form,
                                                  'formset': formset,
                                                  'title': 'Add Item'})


@login_required
def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if item.chef != request.user:
        return HttpResponseForbidden()

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3, max_num=3)

    if request.method == 'POST':
        item_form = ItemForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,
                               queryset=Images.objects.none())

        if item_form.is_valid() and formset.is_valid():

            item = item_form.save(commit=False)
            item.save()

            for form in formset.cleaned_data:
                if form and form['image']:
                    image = form['image']
                    photo = Images(item=item, image=image)
                    photo.save()

            return HttpResponseRedirect(reverse('item:detail', args=(item.id,)))

    else:
        item_form = ItemForm(instance=item)
        formset = ImageFormSet(queryset=Images.objects.filter(item=item))
    return render(request, 'item/add_edit.html', {'item_form': item_form,
                                                  'formset': formset,
                                                  'title': 'Edit Item'})
