# Generated by Django 2.0.3 on 2018-03-25 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_auto_20180325_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='img_big',
            field=models.ImageField(blank=True, upload_to='big', verbose_name='изображение (большое)'),
        ),
        migrations.AlterField(
            model_name='item',
            name='img_small',
            field=models.ImageField(blank=True, upload_to='preview', verbose_name='изображение (маленькое)'),
        ),
    ]
