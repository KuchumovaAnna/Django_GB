# Generated by Django 2.0.3 on 2018-04-01 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basketapp', '0002_auto_20180401_0945'),
    ]

    operations = [
        migrations.AlterField(
            model_name='iteminbasket',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Item'),
        ),
        migrations.AlterField(
            model_name='pastpurchases',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Item'),
        ),
    ]
