# Generated by Django 4.0.4 on 2022-06-01 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0002_alter_referral_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100, verbose_name='Назва ресторану')),
                ('longitude', models.FloatField(verbose_name='Довгота')),
                ('latitude', models.FloatField(verbose_name='Широта')),
            ],
            options={
                'verbose_name': 'Ресторан',
                'verbose_name_plural': 'Ресторани',
            },
        ),
    ]
