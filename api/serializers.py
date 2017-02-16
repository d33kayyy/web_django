from django.contrib.auth.models import User
from rest_framework import serializers

from item.models import Item
from order.models import Order, ItemOrder
from reviews.models import Review
from users.models import UserProfile


class ReviewSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="api:review-detail", lookup_field='pk', read_only=True)
    reviewer = serializers.ReadOnlyField(source='reviewer.id')
    item_id = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = Review
        fields = ['id', 'reviewer', 'item_id', 'content', 'rating', 'updated_time']


class ItemSerializer(serializers.HyperlinkedModelSerializer):
    shop_id = serializers.ReadOnlyField(source='shop.id', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='api:item-detail', lookup_field='pk', read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ['id', 'shop_id', 'name', 'slug', 'price', 'ingredient', 'description', 'in_stock', 'pub_date',
                  'modified_date', 'rating', 'reviews', 'url']
        read_only_fields = ('id', 'slug', 'pub_date', 'modified_date', 'rating')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # items = serializers.HyperlinkedRelatedField(many=True, view_name='api:item-detail', read_only=True)
    items = ItemSerializer(many=True, read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name="api:shop-detail", lookup_field='pk', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'items', 'url']


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'avatar', 'gender', 'birthday', 'email', 'phone', 'allergy', 'point', 'address', 'city',
                  'district', 'ward', 'info', 'user_id']
        read_only_fields = ('id', 'name', 'avatar', 'birthday', 'point', 'user_id')


class ItemOrderSerializer(serializers.ModelSerializer):
    item = serializers.ReadOnlyField(source='item.id')

    class Meta:
        model = ItemOrder
        fields = ['item', 'quantity']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="api:order-detail", lookup_field='pk', read_only=True)
    items = ItemOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'order_id', 'receiver', 'order_date', 'items', 'total_price', 'shipping', 'note',
                  'status', 'phone', 'email', 'address', 'city', 'district', 'ward', 'url']
        read_only_fields = ('id', 'order_id', 'total_price', 'shipping', 'status')
