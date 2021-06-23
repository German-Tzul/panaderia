from django.contrib import admin

# Register your models here.

from panaderia.models import *

admin.site.register(InventarioProducto)
admin.site.register(Compras)
admin.site.register(DetalleCompras)
admin.site.register(ProductoUtilizado)
admin.site.register(ProductoRealizado)
admin.site.register(Factura)
admin.site.register(DetalleFactura)


