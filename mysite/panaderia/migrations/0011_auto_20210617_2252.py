# Generated by Django 3.2.4 on 2021-06-17 22:52

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('panaderia', '0010_auto_20210617_1929'),
    ]

    operations = [
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proveedor', models.CharField(blank=True, max_length=50, null=True)),
                ('factura', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='DetalleCompras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.CharField(choices=[('Quintal', 'Quintal'), ('Libra', 'Libra')], max_length=7)),
                ('cantidad', models.PositiveIntegerField()),
                ('factura', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='panaderia.compras')),
                ('inventario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panaderia.inventarioproducto')),
            ],
        ),
        migrations.DeleteModel(
            name='ComprasProducto',
        ),
    ]
