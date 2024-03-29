# Generated by Django 4.0.4 on 2022-07-28 16:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0016_user_is_chef_user_is_courier'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='connected_restaurant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.restaurant', to_field='name', verbose_name='Ресторан'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Назва'),
        ),
        migrations.AlterField(
            model_name='order',
            name='shipping_address_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.restaurant', to_field='name'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
