# Generated by Django 3.2.5 on 2021-08-11 23:11

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(db_index=True, default=False)),
                ('create_timestamp', models.DateTimeField(auto_now_add=True)),
                ('modify_timestamp', models.DateTimeField(auto_now=True)),
                ('delete_timestamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('first_name', models.CharField(help_text='Please Enter Your First Name.', max_length=100, verbose_name='First Name')),
                ('last_name', models.CharField(help_text='Please Enter Your Last Name.', max_length=100, verbose_name='Last Name')),
                ('phone_number', models.CharField(help_text='Please Enter Your Phone Number', max_length=11, validators=[core.validators.Validators.check_phone_number], verbose_name='Phone Number')),
                ('email', models.EmailField(blank=True, help_text='Please Enter Your Email Address(Optional).', max_length=254, null=True, verbose_name='Email Address')),
                ('text', models.TextField(help_text='Please Write Your Message Text...', verbose_name='Message Text')),
            ],
            options={
                'verbose_name': 'Message',
                'verbose_name_plural': 'Messages',
            },
        ),
    ]
