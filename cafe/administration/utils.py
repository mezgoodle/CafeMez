from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from .models import Place, Restaurant, User, Referral, Purchase, Item, SubCategory, Category


def set_permissions(user: User):
    if user.is_staff:
        needed_models = [Place, Restaurant, Referral, Purchase, Item, Category, SubCategory]
        for model in needed_models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for permission in permissions:
                user.user_permissions.add(permission)
