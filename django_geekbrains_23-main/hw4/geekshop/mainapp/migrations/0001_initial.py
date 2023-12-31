# Generated by Django 2.0.3 on 2018-03-25 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='full_description',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(verbose_name='полное описание')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='имя')),
                ('img', models.ImageField(blank=True, upload_to='', verbose_name='изображение')),
                ('short_desc', models.TextField(blank=True, verbose_name='краткое описание')),
                ('vendor_code', models.CharField(max_length=25, unique=True, verbose_name='артикул')),
            ],
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='имя подкатегории')),
                ('idx', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['parent_name', 'idx'],
            },
        ),
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='имя категории')),
                ('idx', models.PositiveIntegerField(default=0, unique=True)),
                ('color', models.CharField(default='000000', max_length=6, verbose_name='цвет категории')),
            ],
            options={
                'ordering': ['idx'],
            },
        ),
        migrations.CreateModel(
            name='price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(max_length=25, unique=True, verbose_name='артикул')),
                ('price', models.DecimalField(blank=0, decimal_places=2, max_digits=8, verbose_name='цена')),
                ('price_unit', models.CharField(max_length=5, verbose_name='валюта')),
                ('date', models.DateField(auto_now_add=True, verbose_name='дата присвоения цены')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='quantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_code', models.CharField(max_length=25, unique=True, verbose_name='артикул')),
                ('quantity', models.DecimalField(blank=0, decimal_places=0, max_digits=8, verbose_name='цена')),
                ('datetime', models.TimeField(auto_now_add=True, verbose_name='дата и время изменения количества')),
            ],
            options={
                'ordering': ['-datetime'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='quantity',
            unique_together={('vendor_code', 'datetime')},
        ),
        migrations.AlterUniqueTogether(
            name='price',
            unique_together={('vendor_code', 'date')},
        ),
        migrations.AddField(
            model_name='itemcategory',
            name='parent_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ParentCategory'),
        ),
        migrations.AddField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.ItemCategory'),
        ),
        migrations.AddField(
            model_name='full_description',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Item'),
        ),
    ]
