from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from silisili import settings
from .models import Item, Images
from .forms import ItemForm, ImageForm, ImageInlineFormSet


class HomePageView(ListView):
    template_name = 'index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by('-pub_date').all()


class IndexView(ListView):
    template_name = 'item/index.html'
    context_object_name = 'list_items'

    def get_queryset(self):
        """Return the last five published questions."""
        return Item.objects.order_by('-pub_date').all()


class ItemDetailView(DetailView):
    model = Item
    template_name = 'item/detail.html'


# class ItemRedirectDetailView(RedirectView):
#     def get(self, request, *args, **kwargs):
#         pk = self.kwargs.get('pk', None)
#         item = Item.objects.get(pk=pk)
#         self.url = reverse('item:detail', kwargs={'pk': item.pk, 'slug': item.slug})
#         return super(ItemRedirectDetailView, self).get(request, *args, **kwargs)


class CreateItemView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'item/add_edit.html'
    success_message = 'Item successfully created'

    def form_valid(self, form):
        item = form.save(commit=False)
        item.chef = self.request.user
        return super(CreateItemView, self).form_valid(form)


class EditItemView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
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

            return HttpResponseRedirect(reverse('item:detail', args=(item.slug,)))

    else:
        item_form = ItemForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'item/add_edit.html', {'item_form': item_form,
                                                  'formset': formset,
                                                  'title': 'Add Item'})


@login_required
def edit_item(request, slug):
    item = get_object_or_404(Item, slug=slug)

    if item.chef != request.user:
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
    item = get_object_or_404(Item, slug=slug)

    if item.chef != request.user:
        raise PermissionDenied

    item.delete()
    return HttpResponseRedirect(reverse('item:index'))


class CreateReviewView():
    pass