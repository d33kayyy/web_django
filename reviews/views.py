from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import ListView

from order.models import ItemOrder
from reviews.models import Review
from .forms import ReviewForm


# Create your views here.

# @login_required
# def review_display(request):
#
#     # Not reviewed item order (item)
#     item_order = ItemOrder.objects.filter(order__customer=request.user.profile,
#                                           is_reviewed=False,
#                                           order__status='FI')
#     form = ReviewForm
#
#     return render(request, 'reviews/review.html', {'item_order': item_order, 'form': form})

class ReviewPageView(ListView,LoginRequiredMixin):
    '''
    Display all item order that is not reviewed
    '''
    model = ItemOrder
    template_name = 'reviews/review.html'
    context_object_name = 'item_order'

    def get_queryset(self):
        item_order = ItemOrder.objects.filter(order__userprofile=self.request.user.profile,
                                              is_reviewed=False,
                                              order__status='FI')

        return item_order


class ItemReview(FormView, LoginRequiredMixin):
    '''
    Handle review form
    '''
    form_class = ReviewForm

    def get(self, request, *args, **kwargs):
        return HttpResponseBadRequest()

    def form_valid(self, form):
        review = form.save(commit=False)

        item = form.cleaned_data['item']
        reviewer = self.request.user.profile

        if Review.objects.filter(item=item, reviewer=reviewer).exists():
            # Override the old review
            review = Review.objects.get(item=item, reviewer=reviewer)
            review.content = form.cleaned_data['content']
            review.rating = form.cleaned_data['rating']
            review.save()
        else:
            review.reviewer = reviewer
            review.save()

        # Mark as reviewed
        # item_order_id = form.cleaned_data['item_order_id']
        # item_order = ItemOrder.objects.get(id=item_order_id)
        # item_order.is_reviewed = True
        # item_order.save()

        return HttpResponseRedirect(reverse('item:detail', kwargs={'slug': item.slug}))
