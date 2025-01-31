# Generated by Django 5.0.2 on 2024-11-03 11:22

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accessory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('image', models.ImageField(upload_to='accessory_images/')),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_rented', models.BooleanField(default=False)),
                ('image', models.ImageField(upload_to='car_images/')),
                ('description', models.TextField()),
                ('mileage', models.IntegerField(blank=True, null=True)),
                ('fuel_type', models.CharField(choices=[('petrol', 'Бензин'), ('diesel', 'Дизель'), ('electric', 'Электрический'), ('hybrid', 'Гибрид')], default='petrol', max_length=50)),
                ('transmission', models.CharField(choices=[('manual', 'Механическая'), ('automatic', 'Автоматическая')], default='manual', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('accessory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars_app.accessory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('avatar', models.ImageField(default='default_avatar.png', upload_to='avatars/')),
                ('is_seller', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('return_date', models.DateField()),
                ('total_price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cars_app.car')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=100)),
                ('rating', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='cars_app.car')),
            ],
        ),
    ]
