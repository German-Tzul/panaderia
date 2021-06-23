from django.forms import (ModelForm, TextInput, Select,
                          NumberInput)
from django.forms import inlineformset_factory

from panaderia.models import (Compras, DetalleCompras, ProductoUtilizado, 
                              Factura, DetalleFactura)


class ComprasForm(ModelForm):
    class Meta:
        model = Compras
        fields = ['proveedor', 'factura']


class DetalleComprasForm(ModelForm):
    class Meta:
        model = DetalleCompras
        fields = ['inventario', 'peso', 'cantidad']
DetalleComprasInlineFormset = inlineformset_factory(Compras, DetalleCompras, 
                              form=DetalleComprasForm)


class ProductoUtilizadoForm(ModelForm):
    class Meta:
        model = ProductoUtilizado
        fields = ['inventario', 'peso', 'cantidad']
        widgets = {
            'inventario': Select(attrs={'class':'form-control'}),
            'peso': Select(attrs={'class':'form-control'}),
            'cantidad': NumberInput(attrs={'class': 'form-control'}),
        }

# 6
class FacturaForm(ModelForm):
    class Meta:
        model = Factura
        fields = ['nombre', 'nit', 'fecha']
        widgets = {
            'nombre': TextInput(attrs={'class':'form-control'}),
            'nit': TextInput(attrs={'class':'form-control'}),
            'fecha': TextInput(attrs={'class': 'form-control',
            'type':'date'}),
        }

# 7
class DetalleFacturaForm(ModelForm):
    class Meta:
        model = DetalleFactura
        fields = ['producto', 'cantidad', 'precio', 'sub_total']
DetalleFacturaInlineFormset = inlineformset_factory(Factura, DetalleFactura, 
                              form=DetalleFacturaForm)

                             


                              





        

