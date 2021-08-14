# Generated by Django 3.2.5 on 2021-08-14 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_discount_has_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brand',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Create TimeStamp'),
        ),
        migrations.AlterField(
            model_name='brand',
            name='modify_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Modify TimeStamp'),
        ),
        migrations.AlterField(
            model_name='category',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Create TimeStamp'),
        ),
        migrations.AlterField(
            model_name='category',
            name='modify_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Modify TimeStamp'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Create TimeStamp'),
        ),
        migrations.AlterField(
            model_name='discount',
            name='modify_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Modify TimeStamp'),
        ),
        migrations.AlterField(
            model_name='product',
            name='create_timestamp',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Create TimeStamp'),
        ),
        migrations.AlterField(
            model_name='product',
            name='modify_timestamp',
            field=models.DateTimeField(auto_now=True, verbose_name='Modify TimeStamp'),
        ),
    ]
