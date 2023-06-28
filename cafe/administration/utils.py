from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

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


def set_permissions(user: User):
    if user.is_staff:
        needed_models = [
            Place,
            Restaurant,
            Referral,
            Item,
            Category,
            SubCategory,
            Order,
            OrderItem,
        ]
        for model in needed_models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            for permission in permissions:
                user.user_permissions.add(permission)
