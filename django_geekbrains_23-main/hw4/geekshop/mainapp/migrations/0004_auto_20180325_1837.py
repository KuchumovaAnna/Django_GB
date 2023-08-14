# Generated by Django 2.0.3 on 2018-03-25 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0003_auto_20180325_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='instock',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(blank=0, decimal_places=2, default=0, max_digits=8, verbose_name='цена'),
        ),
        migrations.AddField(
            model_name='item',
            name='price_unit',
            field=models.CharField(default='руб', max_length=5, verbose_name='валюта'),
        ),
    ]