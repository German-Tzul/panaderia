# Generated by Django 3.2.4 on 2021-06-16 02:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0003_comprasproducto_inventarioproducto'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprasproducto',
            name='fecha',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 6, 16, 2, 42, 40, 212803, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='comprasproducto',
            name='peso',
            field=models.CharField(choices=[('Quintal', 'Quintal'), ('Libra', 'Libra')], max_length=7),
        ),
    ]
