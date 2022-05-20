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
