# Generated by Django 4.0.4 on 2022-05-22 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='referral',
            name='id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='administration.user', verbose_name='Користувач'),
        ),
    ]