# Generated by Django 4.0.4 on 2022-07-29 16:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0018_order_is_ready'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='connected_courier',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='courier', to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
