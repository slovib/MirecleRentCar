# Generated by Django 5.0.2 on 2024-11-03 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars_app', '0003_alter_order_quantity'),
    ]

    operations = [
        migrations.AddField(
            model_name='accessory',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
