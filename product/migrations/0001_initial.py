# Generated by Django 3.2.5 on 2021-08-03 17:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('title_en', models.CharField(help_text='Please Enter the Title of the Name in English', max_length=100, unique=True, verbose_name='English Title')),
                ('title_fa', models.CharField(help_text='Please Enter the Title of the Name in Persian', max_length=100, unique=True, verbose_name='Persian Title')),
                ('slug', models.SlugField(help_text='Please Type Your Slug', verbose_name='Slug')),
                ('logo', models.FileField(blank=True, default='Unknown.jpg', help_text='Please Upload the Logo Icon of Brand', upload_to='product/brands/', verbose_name='Logo')),
                ('link', models.URLField(blank=True, default=None, help_text='Please Enter Your Website Address', null=True, validators=[django.core.validators.URLValidator], verbose_name='Website Address')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('title_en', models.CharField(help_text='Please Enter the Title of the Name in English', max_length=100, unique=True, verbose_name='English Title')),
                ('title_fa', models.CharField(help_text='Please Enter the Title of the Name in Persian', max_length=100, unique=True, verbose_name='Persian Title')),
                ('slug', models.SlugField(help_text='Please Type Your Slug', verbose_name='Slug')),
                ('properties', models.CharField(default=None, max_length=24, null=True)),
                ('root', models.ForeignKey(blank=True, default=None, help_text='Please Select the Main Category', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subcategories', to='product.category', verbose_name='Main Category')),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('title_en', models.CharField(help_text='Please Enter the Title of the Name in English', max_length=100, unique=True, verbose_name='English Title')),
                ('title_fa', models.CharField(help_text='Please Enter the Title of the Name in Persian', max_length=100, unique=True, verbose_name='Persian Title')),
                ('slug', models.SlugField(help_text='Please Type Your Slug', verbose_name='Slug')),
                ('unit', models.CharField(choices=[('P', 'Percent'), ('T', 'Toman')], help_text='Please Select the Discount Unit', max_length=1, verbose_name='Unit')),
                ('amount', models.PositiveBigIntegerField(default=0, help_text='Please Enter Discount Amount', verbose_name='Discount Amount')),
                ('roof', models.PositiveBigIntegerField(blank=True, default=None, help_text='Please Enter Discount Ceiling(Optional)', null=True, verbose_name='Discount Ceiling')),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, help_text='Please Select the Start Date of the Discount', null=True, verbose_name='Start Date')),
                ('end_date', models.DateTimeField(blank=True, default=None, help_text='Please Select the End Date of the Discount', null=True, verbose_name='End Date')),
            ],
            options={
                'verbose_name': 'Discount',
                'verbose_name_plural': 'Discounts',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('title_en', models.CharField(help_text='Please Enter the Title of the Name in English', max_length=100, unique=True, verbose_name='English Title')),
                ('title_fa', models.CharField(help_text='Please Enter the Title of the Name in Persian', max_length=100, unique=True, verbose_name='Persian Title')),
                ('slug', models.SlugField(help_text='Please Type Your Slug', verbose_name='Slug')),
                ('image', models.FileField(blank=True, default='Unknown.jpg', help_text='Please Upload a Picture of the Product Item', upload_to='product/products/', verbose_name='Picture')),
                ('price', models.PositiveBigIntegerField(help_text='Please Enter the Price of Product Item without Apply Discount', verbose_name='Price')),
                ('inventory', models.PositiveBigIntegerField(help_text='Please Enter the Number of this Product Item into the Stock', verbose_name='Number of Inventory')),
                ('properties', models.CharField(default=None, max_length=24, null=True)),
                ('brand', models.ForeignKey(help_text='Please Select the Brand of the Product Item', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.brand', verbose_name='Brand')),
                ('category', models.ForeignKey(help_text='Please Select the Category of the Product Item', on_delete=django.db.models.deletion.CASCADE, related_name='products', to='product.category', verbose_name='Category')),
                ('discount', models.ForeignKey(blank=True, default=None, help_text='Please Select the Type of Discount if Available', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.discount', verbose_name='Discount')),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
