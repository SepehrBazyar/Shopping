# Generated by Django 3.2.5 on 2021-08-12 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='has_code',
            field=models.BooleanField(db_index=True, default=False, help_text='Please Select Check Box if is the Discount Code else Do Nothing.', verbose_name='Has Code'),
        ),
    ]