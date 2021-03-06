from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView

from .forms import ItemForm, ImageForm, ImageInlineFormSet
from .models import Item, Images


class HomePageView(ListView):
    """
    Homepage
    """
    template_name = 'index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return all items"""
        return Item.objects.order_by('-created_date').all()


class IndexView(ListView):
    """
    List of all items (possibly for searching)
    """
    template_name = 'item/index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return all the items"""
        return Item.objects.order_by('-pub_date').all()


class ItemDetailDisplay(DetailView):
    """
    Item detail page
    """
    model = Item
    template_name = 'item/detail.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailDisplay, self).get_context_data(**kwargs)
        context['rating'] = range(int(self.object.get_rating()))
        return context


def career(request):
    return render(template_name='work.html', request=request)


def pin(request):
    return render(template_name='pin.html', request=request)


@login_required
def create_item(request):
    """
    Create item page for shop
    """
    if not request.user.profile.is_shop:
        raise PermissionDenied

    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=3, max_num=3)

    if request.method == 'POST':

        item_form = ItemForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if item_form.is_valid() and formset.is_valid():

            item = item_form.save(commit=False)
            item.shop = request.user
            item.save()

            for form in formset.cleaned_data:
                if form and form['image']:
                    image = form['image']
                    photo = Images(item=item, image=image)
                    photo.save()

            return HttpResponseRedirect(reverse('item:detail', args=(item.slug,)))

    else:
        item_form = ItemForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'item/add_edit.html', {'item_form': item_form,
                                                  'formset': formset,
                                                  'title': 'Add Item'})


@login_required
def edit_item(request, slug):
    """
    Edit item page
    """
    item = get_object_or_404(Item, slug=slug)

    if item.shop != request.user or not request.user.profile.is_shop:
        raise PermissionDenied

    if request.method == 'POST':
        item_form = ItemForm(request.POST, instance=item)
        formset = ImageInlineFormSet(request.POST, request.FILES)

        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.save()

            formset = ImageInlineFormSet(request.POST, request.FILES, instance=item)

            if formset.is_valid():
                formset.save()

                return HttpResponseRedirect(reverse('item:detail', args=(item.slug,)))

    else:
        item_form = ItemForm(instance=item)
        formset = ImageInlineFormSet(instance=item)
    return render(request, 'item/add_edit.html', {'item_form': item_form,
                                                  'formset': formset,
                                                  'title': 'Edit Item'})


@login_required
def delete_item(request, slug):
    """
    Delete item handler
    """
    item = get_object_or_404(Item, slug=slug)

    if item.shop != request.user or not request.user.profile.is_shop:
        raise PermissionDenied

    item.delete()
    return HttpResponseRedirect(reverse('item:index'))
