# Generated by Django 3.2 on 2023-09-25 11:13

import apps.authentication.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('supplier_name', models.CharField(max_length=255, unique=True)),
                ('manufacturer_number', models.TextField(blank=True, null=True)),
                ('vendor_number', models.TextField(blank=True, null=True)),
                ('last_p_n', models.TextField(blank=True, null=True)),
                ('atech', models.BooleanField(default=False)),
                ('jegs', models.BooleanField(default=False)),
                ('speedway', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('relationship_status', models.TextField(blank=True, null=True)),
                ('initial', models.TextField(blank=True, null=True)),
                ('supplier', models.TextField(blank=True, null=True)),
                ('website', models.TextField(blank=True, null=True)),
                ('account_numbers', models.TextField(blank=True, null=True)),
                ('log_on_info', models.TextField(blank=True, null=True)),
                ('phone', models.TextField(blank=True, null=True)),
                ('user_address', models.TextField(blank=True, null=True)),
                ('city_state_zip_code', models.TextField(blank=True, null=True)),
                ('contact_name', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_email', models.EmailField(max_length=255, unique=True)),
                ('contact_phone', models.TextField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_vendor', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('first_name', models.CharField(blank=True, max_length=255)),
                ('last_name', models.CharField(blank=True, max_length=255)),
                ('profile_picture', models.ImageField(blank=True, upload_to=apps.authentication.models.user_directory_path, verbose_name='Profile Picture')),
                ('gender', models.CharField(blank=True, choices=[('m', 'Male'), ('f', 'Female'), ('0', 'Other')], max_length=1)),
                ('about', models.TextField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('auth_provider', models.CharField(default='email', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
