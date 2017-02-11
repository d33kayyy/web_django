from django.contrib.auth.models import User
from rest_framework import generics, permissions

from item.models import Item
from users.models import UserProfile
from .permissions import IsOwnerOrReadOnly, IsShopOrReadOnly, IsOwner
from .serializers import ItemSerializer, UserSerializer, UserProfileSerializer


class ItemList(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsShopOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(shop=self.request.user)


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwner,)

    def get_object(self, queryset=None):
        return self.request.user.profile
