# Generated by Django 3.2.12 on 2022-04-04 13:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_merge_0016_billingaddress_0016_subscribe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='order',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='billing', to='product.order'),
        ),
    ]
