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
    name = models.CharField(max_length=100, verbose_name='Назва ресторану', unique=True)
    longitude = models.FloatField(verbose_name='Довгота')
    latitude = models.FloatField(verbose_name='Широта')

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Ресторани'

    def __str__(self):
        return f'Ресторан {self.id} - {self.name}'


class Place(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    free = models.BooleanField(default=True, verbose_name='Вільне місце')
    restaurant = models.ForeignKey(Restaurant, to_field='name', on_delete=models.CASCADE, verbose_name='Ресторан',
                                   default='МакДональдз. Метро Вокзальна')

    class Meta:
        verbose_name = 'Місце'
        verbose_name_plural = 'Місця'

    def __str__(self):
        return f'Місце {self.id} у ресторані {self.restaurant} - {"Вільне" if self.free else "Зайняте"}'


class User(TimeStampedModel, AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, verbose_name='Ім\'я користувача в телеграмі', unique=True)
    email = models.EmailField(max_length=100, verbose_name='Електронна пошта', unique=True)
    telegram_id = models.IntegerField(verbose_name='Ідентифікатор користувача у телеграмі',
                                      default=353057906, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f'#{self.id} @{self.username}'


class Referral(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name='Ідентифікатор користувача у телеграмі',
                                  default=353057906, unique=True)
    referrer_id = models.ForeignKey(User, to_field='telegram_id', on_delete=models.CASCADE,
                                    verbose_name='Користувач')

    class Meta:
        verbose_name = 'Реферал'
        verbose_name_plural = 'Реферали'

    def __str__(self):
        return f'{self.user_id} прийшов від {self.referrer_id.username}'


class Category(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Назва', unique=True)
    code = models.CharField(max_length=20, verbose_name='Код')

    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural = 'Категорії'

    def __str__(self):
        return f'{self.name}'


class SubCategory(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Назва', unique=True)
    code = models.CharField(max_length=20, verbose_name='Код')
    category = models.ForeignKey(Category, to_field='name', on_delete=models.CASCADE, verbose_name='Категорія')

    class Meta:
        verbose_name = 'Підкатегорія'
        verbose_name_plural = 'Підкатегорії'

    def __str__(self):
        return f'{self.name}'


class Item(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50, verbose_name='Назва')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Ціна')
    description = models.TextField(verbose_name='Опис', null=True, max_length=200)
    photo = models.CharField(max_length=250, verbose_name='Фото file_id')
    subcategory = models.ForeignKey(SubCategory, to_field='name', on_delete=models.CASCADE, verbose_name='Підкатегорія',
                                    default='Перші страви')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукти'

    def __str__(self):
        return f'#{self.id} - {self.name}'


class Purchase(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, on_delete=models.SET(0), verbose_name='Користувач')
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Продукт')
    amount = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Вартість')
    quantity = models.IntegerField(verbose_name='Кількість')
    purchase_time = models.DateTimeField(verbose_name='Час покупки', auto_now_add=True)
    shipping_address = models.CharField(max_length=200, verbose_name='Адреса доставки', null=True)
    email = models.EmailField(max_length=100, verbose_name='Електронна пошта')
    reciever = models.CharField(max_length=100, verbose_name='Ім\'я отримувача')
    successfull = models.BooleanField(default=False, verbose_name='Успішна оплата')

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        return f'#{self.id} - {self.item_id} ({self.quantity})'
