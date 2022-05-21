# Generated by Django 4.0.4 on 2022-05-21 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Назва')),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Ціна')),
                ('description', models.TextField(max_length=200, null=True, verbose_name='Опис')),
                ('photo', models.CharField(max_length=200, verbose_name='Фото file_id')),
                ('category_code', models.CharField(max_length=20, verbose_name='Код категорії')),
                ('category_name', models.CharField(max_length=20, verbose_name='Назва категорії')),
                ('subcategory_code', models.CharField(max_length=20, verbose_name='Код підкатегорії')),
                ('subcategory_name', models.CharField(max_length=20, verbose_name='Назва підкатегорії')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукти',
            },
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('free', models.BooleanField(default=True, verbose_name='Вільне місце')),
            ],
            options={
                'verbose_name': 'Місце',
                'verbose_name_plural': 'Місця',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.BigIntegerField(default=1, unique=True, verbose_name='Ідентифікатор користувача у телеграмі')),
                ('name', models.CharField(max_length=100, verbose_name="Ім'я користувача")),
                ('username', models.CharField(max_length=100, verbose_name="Ім'я користувача в телеграмі")),
                ('email', models.EmailField(max_length=100, verbose_name='Електронна пошта')),
            ],
            options={
                'verbose_name': 'Користувач',
                'verbose_name_plural': 'Користувачі',
            },
        ),
        migrations.CreateModel(
            name='Referral',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='adminmanage.user', unique=True, verbose_name='Користувач')),
                ('referrer_id', models.BigIntegerField()),
            ],
            options={
                'verbose_name': 'Реферал',
                'verbose_name_plural': 'Реферали',
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Вартість')),
                ('quantity', models.IntegerField(verbose_name='Кількість')),
                ('purchase_time', models.DateTimeField(auto_now_add=True, verbose_name='Час покупки')),
                ('shipping_address', models.CharField(max_length=200, null=True, verbose_name='Адреса доставки')),
                ('email', models.EmailField(max_length=100, verbose_name='Електронна пошта')),
                ('reciever', models.CharField(max_length=100, verbose_name="Ім'я отримувача")),
                ('successfull', models.BooleanField(default=False, verbose_name='Успішна оплата')),
                ('buyer', models.ForeignKey(on_delete=models.SET(0), to='adminmanage.user', verbose_name='Користувач')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminmanage.item', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Покупка',
                'verbose_name_plural': 'Покупки',
            },
        ),
    ]