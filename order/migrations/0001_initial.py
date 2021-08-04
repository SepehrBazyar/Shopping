# Generated by Django 3.2.5 on 2021-08-04 16:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0001_initial'),
        ('customer', '0003_auto_20210804_1437'),
    ]

    operations = [
        migrations.CreateModel(
            name='DiscountCode',
            fields=[
                ('discount_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='product.discount')),
                ('code', models.CharField(help_text='Please Enter Identification Code to Check Validation in Order Model', max_length=10, unique=True, verbose_name='Identification Code')),
                ('users', models.ManyToManyField(default=None, help_text='Show Which Users have Used this Code?', null=True, related_name='codes', to='customer.Customer', verbose_name='Users Used')),
            ],
            options={
                'verbose_name': 'Discount Code',
                'verbose_name_plural': 'Discount Codes',
            },
            bases=('product.discount',),
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('status', models.CharField(choices=[('P', 'Paid'), ('U', 'Unpaid'), ('C', 'Canceled')], default='U', help_text='Please Select the Status of Order(By Default Unpaid is Considered)', max_length=1, verbose_name='Status of Order')),
                ('total_price', models.PositiveBigIntegerField(default=0, help_text='Total Price is Sum of Pure Price of Product Items for this Order', verbose_name='Total Price')),
                ('final_price', models.PositiveBigIntegerField(default=0, help_text='Final Price is Sum of Price of Product Items for this Order After Dicount', verbose_name='Final Price')),
                ('code', models.CharField(blank=True, default=None, help_text='If You have a Discount Code Please Enter it', max_length=10, null=True, verbose_name='Discount Code')),
                ('customer', models.ForeignKey(help_text='Please Select Customer Owner this Order', on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='customer.customer', verbose_name='Customer')),
                ('discount', models.ForeignKey(default=None, help_text='Please Select Discount from Discount Codes to Apply on Price', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='order.discountcode', verbose_name='Discount Value')),
            ],
            options={
                'verbose_name': 'Order',
                'verbose_name_plural': 'Orders',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('count', models.PositiveIntegerField(default=1, help_text='Please Selcet the Count of this Order Item(Minimum Value is 1).', verbose_name='Count of Order Item')),
                ('order', models.ForeignKey(help_text='Please Select Your Order', on_delete=django.db.models.deletion.CASCADE, related_name='items', to='order.order', verbose_name='Recepite Order')),
                ('product', models.ForeignKey(help_text='Please Select Product Item to Add', on_delete=django.db.models.deletion.CASCADE, related_name='+', to='product.product', verbose_name='Product Item')),
            ],
            options={
                'verbose_name': 'Order Item',
                'verbose_name_plural': 'Order Items',
            },
        ),
    ]
