from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse

from item.models import Item
from order.models import Order
from reviews.models import Review
from users.models import UserProfile
from .permissions import IsOwnerOrReadOnly, IsShopOrReadOnly, IsOwner
from .serializers import ItemSerializer, UserSerializer, UserProfileSerializer, ReviewSerializer, OrderSerializer


class ItemGenericView(generics.GenericAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class ItemList(generics.ListCreateAPIView, ItemGenericView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView, ItemGenericView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserGenericView(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserList(generics.ListAPIView, UserGenericView):
    pass


class UserDetail(generics.RetrieveAPIView, UserGenericView):
    pass


class UserProfileDetail(generics.RetrieveAPIView):
    """
    No update yet. Must figure out a way to restrict write access to some fields
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner,)

    def get_object(self, queryset=None):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated
        return self.request.user.profile


class ShopGenericView(generics.GenericAPIView):
    queryset = User.objects.filter(profile__is_shop=True)
    serializer_class = UserSerializer


class ShopList(generics.ListAPIView, ShopGenericView):
    pass


class ShopDetail(generics.RetrieveAPIView, ShopGenericView):
    pass


# class ReviewDetail(generics.RetrieveAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
#     lookup_field = 'pk'

class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def perform_create(self, serializer):
    #     if
    #     serializer.save(shop=self.request.user)


class OrderGenericView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Order.objects.filter(userprofile=self.request.user.profile)


class OrderListView(generics.ListCreateAPIView, OrderGenericView):
    pass


class OrderDetailView(generics.RetrieveAPIView, OrderGenericView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)


# class ItemViewSet(viewsets.ModelViewSet):
#     """
#     This viewset automatically provides `list`, `create`, `retrieve`,
#     `update` and `destroy` actions.
#     """
#     queryset = Item.objects.all()
#     serializer_class = ItemSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly, IsOwnerOrReadOnly,)
#
#     def perform_create(self, serializer):
#         serializer.save(shop=self.request.user)
#
#
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (permissions.IsAdminUser,)
#
#
# class ShopViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     This viewset automatically provides `list` and `detail` actions.
#     """
#     queryset = User.objects.filter(profile__is_shop=True)
#     serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    """
    API root
    """
    api_list = {
        'items': reverse('api:item-list', request=request, format=format),
        'shops': reverse('api:shop-list', request=request, format=format),
    }
    if request.user.is_authenticated:
        api_list['profile'] = reverse('api:profile', request=request, format=format)
        api_list['orders'] = reverse('api:order-list', request=request, format=format)

        if request.user.is_superuser:
            api_list['users'] = reverse('api:user-list', request=request, format=format)

    return Response(api_list)
