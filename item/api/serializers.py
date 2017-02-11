from rest_framework import serializers

from item.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'name', 'slug', 'price', 'ingredient', 'description', 'in_stock', 'pub_date', 'modified_date',
                  'rating']
