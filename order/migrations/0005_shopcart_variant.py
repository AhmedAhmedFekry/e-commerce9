# Generated by Django 3.1.6 on 2021-02-13 11:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_color_productlang_size_variants'),
        ('order', '0004_auto_20210211_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopcart',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.variants'),
        ),
    ]
