from django.contrib import admin

from .models import (
    Category,
    Item,
    Order,
    OrderItem,
    Place,
    Referral,
    Restaurant,
    SubCategory,
    User,
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "is_staff",
        "is_chef",
        "is_courier",
        "is_active",
        "telegram_id",
        "referred",
    )
    list_filter = (
        "is_staff",
        "is_chef",
        "is_courier",
        "is_active",
        "connected_restaurant",
    )
    search_fields = ("email", "telegram_id", "username")
    ordering = ("email",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "subcategory")
    prepopulated_fields = {"description": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code")
    search_fields = ("name", "code")


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "code", "category")
    search_fields = ("name", "code", "category__name")


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ("user_id", "referrer_id", "activated")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "payment_method",
        "total_price",
        "is_paid",
        "is_delivered",
        "is_ready",
        "is_finished",
        "created",
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "item", "order", "quantity", "created")


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ("id", "free", "restaurant")


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
