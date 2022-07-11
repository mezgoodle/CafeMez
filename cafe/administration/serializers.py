from rest_framework import serializers
from rest_framework.relations import HyperlinkedRelatedField

from .models import Place, Restaurant, User, Referral, Item, Category, SubCategory


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        lookup_field = 'code'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items_amount'] = instance.count_items()
        return data


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items_amount'] = instance.count_items()
        return data


class ItemSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(many=False, read_only=True)

    class Meta:
        model = Item
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = '__all__'


class ReferralSerializer(serializers.ModelSerializer):
    class Meta:
        model = Referral
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'password', 'telegram_id']
        extra_kwargs = {'password': {'write_only': True}}
        lookup_field = 'username'
