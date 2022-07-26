# Generated by Django 4.0.4 on 2022-07-26 09:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0007_alter_category_code_alter_category_name_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('paymentMethod', models.CharField(blank=True, choices=[('CH', 'Cash'), ('CD', 'Card')], max_length=200, null=True)),
                ('tax_price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('shipping_price', models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=7, null=True)),
                ('isPaid', models.BooleanField(default=False)),
                ('isDelivered', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
        migrations.AlterField(
            model_name='category',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Код категорії'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Назва категорії'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='code',
            field=models.CharField(max_length=20, unique=True, verbose_name='Код підкатегорії'),
        ),
        migrations.AlterField(
            model_name='subcategory',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Назва підкатегорії'),
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.item')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='administration.order')),
            ],
        ),
    ]
