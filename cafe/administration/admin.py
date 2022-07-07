from django.contrib import admin

from .models import Item, User, Place, Purchase, Referral, Restaurant, Category, SubCategory


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff', 'is_active', 'telegram_id')
    list_filter = ('email', 'is_staff', 'is_active',)
    search_fields = ('email', 'telegram_id', 'username')
    ordering = ('email',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'subcategory')
    prepopulated_fields = {'description': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code')
    search_fields = ('name', 'code')


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'category')
    search_fields = ('name', 'code', 'category__name')


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'referrer_id')


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'item_id', 'quantity', 'reciever', 'created', 'successfull')


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'free', 'restaurant')


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
