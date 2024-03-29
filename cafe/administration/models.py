import decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Назва ресторану", unique=True)
    longitude = models.FloatField(verbose_name="Довгота")
    latitude = models.FloatField(verbose_name="Широта")

    class Meta:
        verbose_name = "Ресторан"
        verbose_name_plural = "Ресторани"

    def __str__(self):
        return f"Ресторан {self.id} - {self.name}"


class User(TimeStampedModel, AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(
        max_length=100, verbose_name="Ім'я користувача в телеграмі", unique=True
    )
    email = models.EmailField(
        max_length=100, verbose_name="Електронна пошта", unique=True
    )
    telegram_id = models.IntegerField(
        verbose_name="Ідентифікатор користувача у телеграмі",
        default=353057906,
        unique=True,
    )
    is_chef = models.BooleanField(default=False, verbose_name="Шеф")
    is_courier = models.BooleanField(default=False, verbose_name="Кур'єр")
    connected_restaurant = models.ForeignKey(
        Restaurant,
        to_field="name",
        on_delete=models.CASCADE,
        verbose_name="Ресторан",
        null=True,
        blank=True,
    )
    referred = models.IntegerField(
        default=0, verbose_name="К-сть людей, що використали його реферал"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Користувач"
        verbose_name_plural = "Користувачі"

    def __str__(self):
        return f"#{self.id} @{self.username}"


class Place(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    free = models.BooleanField(default=True, verbose_name="Вільне місце")
    restaurant = models.ForeignKey(
        Restaurant,
        to_field="name",
        on_delete=models.CASCADE,
        verbose_name="Ресторан",
        default="МакДональдз. Метро Вокзальна",
    )
    customer = models.ForeignKey(
        User,
        to_field="username",
        on_delete=models.CASCADE,
        verbose_name="Замовник",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Місце"
        verbose_name_plural = "Місця"

    def __str__(self):
        return f'Місце {self.id} у ресторані {self.restaurant} - {"Вільне" if self.free else "Зайняте"}'


class Referral(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(
        verbose_name="Ідентифікатор користувача у телеграмі",
        default=353057906,
        unique=True,
    )
    referrer_id = models.ForeignKey(
        User,
        to_field="telegram_id",
        on_delete=models.CASCADE,
        verbose_name="Користувач",
    )
    activated = models.BooleanField(default=False, verbose_name="Активований")

    class Meta:
        verbose_name = "Реферал"
        verbose_name_plural = "Реферали"

    def __str__(self):
        return f"{self.user_id} прийшов від {self.referrer_id.username}"


class Category(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Назва категорії")
    code = models.CharField(max_length=20, verbose_name="Код категорії", unique=True)

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

    def __str__(self):
        return f"{self.name}"

    def count_items(self):
        subcategories = self.subcategory_set.all()
        return sum([subcategory.item_set.count() for subcategory in subcategories])


class SubCategory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Назва підкатегорії")
    code = models.CharField(max_length=20, verbose_name="Код підкатегорії", unique=True)
    category = models.ForeignKey(
        Category, to_field="code", on_delete=models.CASCADE, verbose_name="Категорія"
    )

    class Meta:
        verbose_name = "Підкатегорія"
        verbose_name_plural = "Підкатегорії"

    def __str__(self):
        return f"{self.name}"

    def count_items(self):
        return self.item_set.count()


class Item(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name="Назва", unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Ціна")
    description = models.TextField(verbose_name="Опис", null=True, max_length=200)
    photo = models.CharField(max_length=250, verbose_name="Фото file_id")
    subcategory = models.ForeignKey(
        SubCategory,
        to_field="code",
        on_delete=models.CASCADE,
        verbose_name="Підкатегорія",
        default="Перші страви",
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукти"

    def __str__(self):
        return f"#{self.id} - {self.name}"


class Order(TimeStampedModel):
    PAYMENT_METHOD_CHOICES = [
        ("CH", "Cash"),
        ("CD", "Card"),
    ]

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, to_field="username", on_delete=models.SET_NULL, null=True
    )
    payment_method = models.CharField(
        max_length=200, null=True, blank=True, choices=PAYMENT_METHOD_CHOICES
    )
    shipping_price = models.DecimalField(
        null=True, blank=True, max_digits=4, decimal_places=2
    )
    shipping_address_longitude = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=7
    )
    shipping_address_latitude = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=7
    )
    shipping_address_name = models.ForeignKey(
        Restaurant, to_field="name", on_delete=models.CASCADE, null=True, blank=True
    )
    connected_courier = models.OneToOneField(
        User,
        to_field="username",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name="courier",
    )
    is_paid = models.BooleanField(default=False)
    is_delivered = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    is_finished = models.BooleanField(default=False)

    @property
    def total_price(self):
        if self.orderitem_set.first():
            sum = self.total_price_without_discount
            if (count := self.user.referred) != 0:
                return round(sum - sum * decimal.Decimal(count * 0.5 / 100), 2)
            if Referral.objects.filter(user_id=self.user.telegram_id).first():
                return round(sum - sum * decimal.Decimal(2 / 100), 2)
            return sum

    @property
    def total_price_without_discount(self):
        if self.orderitem_set.first():
            return self.tax_price + self.shipping_price

    @property
    def tax_price(self):
        return sum(
            [item.item.price * item.quantity for item in self.orderitem_set.all()]
        )

    class Meta:
        verbose_name = "Замовлення"
        verbose_name_plural = "Замовлення"
        ordering = ["-created"]

    def __str__(self):
        return f"#{self.id} - {self.user}"

    def get_items(self):
        return self.orderitem_set.all()


class OrderItem(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    item = models.ForeignKey(Item, to_field="name", null=True, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, null=True, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, default=1)

    class Meta:
        verbose_name = "Продукт у замовленні"
        verbose_name_plural = "Продукти у замовленні"

    def __str__(self):
        return f"{self.item} у к-сті {self.quantity}"
