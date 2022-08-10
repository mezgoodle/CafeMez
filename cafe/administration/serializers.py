from rest_framework import serializers

from .models import Place, Restaurant, User, Referral, Item, Category, SubCategory, Order, OrderItem


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'
        lookup_field = 'name'


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


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'
        depth = 1


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
        fields = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'password', 'telegram_id', 'is_chef',
                  'is_courier', 'connected_restaurant']
        extra_kwargs = {'password': {'write_only': True}}
        lookup_field = 'username'


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()
    tax_price = serializers.SerializerMethodField()
    user = UserSerializer(many=False, read_only=True)
    shipping_address_name = RestaurantSerializer(many=False, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['items'] = OrderItemSerializer(instance.get_items(), many=True).data
        return data

    def get_total_price(self, instance):
        return instance.total_price

    def get_tax_price(self, instance):
        return instance.tax_price
