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


class Place(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    free = models.BooleanField(default=True, verbose_name='Вільне місце')

    class Meta:
        verbose_name = 'Місце'
        verbose_name_plural = 'Місця'

    def __str__(self):
        return f'Місце {self.id} - {self.free}'


class User(TimeStampedModel):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(unique=True, default=1, verbose_name='Ідентифікатор користувача у телеграмі')
    name = models.CharField(max_length=100, verbose_name='Ім\'я користувача')
    username = models.CharField(max_length=100, verbose_name='Ім\'я користувача в телеграмі')
    email = models.EmailField(max_length=100, verbose_name='Електронна пошта')

    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'

    def __str__(self):
        return f'#{self.id} ({self.user_id} {self.name})'