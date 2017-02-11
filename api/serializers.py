from django.contrib.auth.models import User
from rest_framework import serializers

from item.models import Item
from users.models import UserProfile


class ItemSerializer(serializers.ModelSerializer):
    shop = serializers.ReadOnlyField(source='shop.id')

    class Meta:
        model = Item
        fields = ['id', 'name', 'slug', 'price', 'ingredient', 'description', 'in_stock', 'pub_date', 'modified_date',
                  'rating', 'shop']


class UserSerializer(serializers.ModelSerializer):
    items = serializers.PrimaryKeyRelatedField(many=True, queryset=Item.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'date_joined', 'items']


class UserProfileSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = UserProfile
        fields = ['id', 'name', 'avatar', 'gender', 'birthday', 'email', 'phone', 'allergy', 'point', 'address', 'city',
                  'district', 'ward', 'is_shop', 'info', 'is_shop', 'slug', 'user_id']
