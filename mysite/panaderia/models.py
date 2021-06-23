from django.db import models
from  django.utils import timezone
from datetime import date

# 1
# inventario de materiales que utiliza la panaderia
class InventarioProducto(models.Model):
    PRODUCTO = [
    ('Arina', 'Arina'),
    ('Azucar', 'Azucar'),
    ('Manteca', 'Manteca'),
    ('Levadura', 'Levadura'),
    ]
    nombre = models.CharField(max_length=20, choices=PRODUCTO)
    # esta registrado por libras deacuerdo a las compras realizadas
    cantidad = models.IntegerField()

    def __str__(self):
        return self.nombre


# Registro de la factura de compras de productos
# El proveedor como el numero de la factura son nulos
# Esto por si la persona no quisiera colocar dicho elementos
class Compras(models.Model):
    proveedor = models.CharField(max_length=50, null=True)
    factura = models.CharField(max_length=50, null=True)
    fecha = models.DateField(default=date.today)
    
    def __str__(self):
        return self.factura

    
# clase que se utilizo para el detalle de compras
# ------------------------------------------------
# cuando es por quintal pasarlo a libras 
# porque cuando se utiliza lo realizan por libras
# comparar peso deacuerdo ha eso calcular libras si es quintal
# y sumarlo al inventario de productos
# calculos realizado en la vista
class DetalleCompras(models.Model):
    # convertir los quintales a libra para mayor control 
    CANTIDAD = [
        ('Quintal', 'Quintal'),
        ('Libra', 'Libra'),
    ]
    # para registrar los nombres de los productos 
    factura = models.ForeignKey(Compras, on_delete=models.CASCADE, null=True)
    inventario = models.ForeignKey(InventarioProducto, on_delete=models.CASCADE)
    peso = models.CharField(max_length=7, choices=CANTIDAD)
    cantidad = models.PositiveIntegerField()
        
    def __str__(self):
        return self.inventario.nombre
        

class MostrarProductoUtilizado(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(fecha__month=6)


#  registro de cada dia de cuantas libras se utiliza por producto
#  al registrarlo restar automaticamente del inventario de productos
class ProductoUtilizado(models.Model):
    CANTIDAD = [
        ('Quintal', 'Quintal'),
        ('Libra', 'Libra'),
    ]
    inventario = models.ForeignKey(InventarioProducto, on_delete=models.CASCADE)
    peso = models.CharField(max_length=7, choices=CANTIDAD)
    cantidad = models.PositiveIntegerField()
    fecha = models.DateTimeField(default=date.today)

    objects = MostrarProductoUtilizado()
    
    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.inventario.nombre
    

# clase para registrar los producto creados
# todos los panes ingresados
# --------------------------------------------------
class ProductoRealizado(models.Model):
    nombre = models.CharField(max_length=60)
    precio = models.DecimalField(max_digits=5, decimal_places=2)
    existencia = models.IntegerField()

    def __str__(self):
        return self.nombre

# 6
class Factura(models.Model):
    nombre = models.CharField(max_length=50)
    nit = models.CharField(max_length=50)
    fecha = models.DateField(default=date.today)
    
    def __str__(self):
        return self.nombre 

# 7
class DetalleFactura(models.Model):
    producto = models.ForeignKey(ProductoRealizado, on_delete=models.CASCADE)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(null=True)
    precio = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    sub_total = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.factura.nombre




    



    



    
