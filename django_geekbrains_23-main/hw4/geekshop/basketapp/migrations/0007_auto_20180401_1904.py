# Generated by Django 2.0.3 on 2018-04-01 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0006_auto_20180401_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userorder',
            name='order',
            field=models.AutoField(primary_key=True, serialize=False, verbose_name='номер ордера покупки'),
        ),
    ]