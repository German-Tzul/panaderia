# Generated by Django 3.2.4 on 2021-06-17 01:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0004_auto_20210616_0242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comprasproducto',
            name='fecha',
            field=models.DateField(blank=True, default=datetime.date(2021, 6, 17), null=True),
        ),
    ]