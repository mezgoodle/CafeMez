# Generated by Django 4.0.4 on 2022-07-26 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0010_alter_orderitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=models.SET(1), to='administration.item'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=models.SET(1), to='administration.order'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
