# Generated by Django 3.2.12 on 2022-02-11 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='tags',
            field=models.ManyToManyField(to='product.Tag'),
        ),
    ]