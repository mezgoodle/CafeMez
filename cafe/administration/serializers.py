from rest_framework import serializers
from .models import Place, Restaurant, User, Referral, Item, Category, SubCategory


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class SubCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True, many=False)

    class Meta:
        model = SubCategory
        fields = '__all__'


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
