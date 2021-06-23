from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView 
from django.views import View
from django.views.generic.edit import FormView 
from django.forms import inlineformset_factory, formset_factory
from django.urls import reverse_lazy
from django.db.models import F
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required

from panaderia.models import (InventarioProducto, Compras, DetalleCompras,
                              ProductoUtilizado, ProductoRealizado, Factura)  
from panaderia.forms import (ComprasForm, DetalleComprasInlineFormset,
                            ProductoUtilizadoForm, FacturaForm, 
                            DetalleFacturaInlineFormset)

# 0
def index(request):
    mensaje = 'hola mundo'
    context = {'mensaje': mensaje }
    return render(request,'panaderia/index.html', context)

    
# 1
# muestra el inventario de la panaderia
class InventarioProductoListView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login/'
    model = InventarioProducto
    context_object_name = 'inventario'
    template_name = 'panaderia/inventario.html'


# muestra las compras realizadas
class DetalleComprasDetailView(LoginRequiredMixin, DetailView):
    login_url = '/accounts/login/'
    model = InventarioProducto
    context_object_name = 'inventario'
    template_name = 'panaderia/productos.html'


class ComprasCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Compras
    form_class = ComprasForm
    context_object_name = 'compras'
    template_name = "panaderia/compras.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            compra = form.save(commit=False)
            compra.save()
            return redirect('panaderia:detalle-compras', compra.id)


@login_required(login_url='/accounts/login/')
def detalle_compras(request, compras_id):
    compras = Compras.objects.get(pk=compras_id)
    if request.method == "POST":
        formset = DetalleComprasInlineFormset(
                                             request.POST, request.FILES, 
                                             instance=compras)
        if formset.is_valid():
            form = formset.save(commit=False)
            for f in form:
                f.save()
                # obtener la pk del inventario 
                pk = f.inventario.pk
                # Realizamos la busqueda en el inventario
                i = InventarioProducto.objects.get(id=pk)
                # Pasamos a libra el quintal
                if f.peso == 'Quintal':
                    libra = f.cantidad * 100
                    i.cantidad = F('cantidad') + libra
                    i.save()
                # El peso es en libras solo sumamos
                else:
                    i.cantidad = F('cantidad') + f.cantidad
                    i.save()    
            return redirect('panaderia:detalle-compras', compras_id=compras.id)
    else:
        formset = DetalleComprasInlineFormset(instance=compras)
    return render(request, 'panaderia/detalle_compras.html', 
                 {'formset': formset})


class ProductoUtilizadoView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'
    model = ProductoUtilizado
    form_class = ProductoUtilizadoForm
    template_name = 'panaderia/producto_utilizado.html'

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):
        context = {}
        context["productos"] = self.get_queryset()
        context["form"] = self.form_class
        return context
    
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())
        
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            # obtenemos la pk del inventario
            inventario_pk = c.inventario.pk
            # realizamos la busqueda en el inventario
            #  para restar el producto utilizado
            inventario = InventarioProducto.objects.get(id=inventario_pk)
            # calculamos y guardamos en el inventario del producto
            if c.peso == 'Quintal':
                    libra = c.cantidad * 100  
                    # verificamos si hay suficiente producto en el inventario
                    if inventario.cantidad > libra:
                        inventario.cantidad = F('cantidad') - libra
                        c.save()
                        inventario.save()
                    else:  
                        # mostramos la cantidad de existencia en libras
                        messages.warning(request, 'No hay productos suficientes ' +
                                        'existncia ' + str(inventario.cantidad) + ' lbs')   
            else:
                # verificamos si hay suficiente producto en el inventario
                if inventario.cantidad > c.cantidad:
                     # calculamos si hay existencia
                    inventario.cantidad = F('cantidad') - c.cantidad
                    c.save()
                    inventario.save() 
                else:
                    # mostramos la cantidad de existencia en libras
                    messages.warning(request, 'No hay productos suficientes ' +
                                        'existencia ' + str(inventario.cantidad) + ' lbs') 
        return redirect('panaderia:producto-utilizado')    


# 6
class FacturaCreateView(LoginRequiredMixin, CreateView):
    login_url = '/accounts/login/'
    model = Factura
    form_class = FacturaForm
    context_object_name = 'factura'
    template_name = "panaderia/factura.html"

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            factura = form.save(commit=False)
            factura.save()
            return redirect('panaderia:detalle-factura', factura.id)


# 7
@login_required(login_url='/accounts/login/')
def detalle_factura(request, factura_id):
    factura = Factura.objects.get(pk=factura_id)
    producto = ProductoRealizado.objects.all()
    if request.method == "POST":
        formset = DetalleFacturaInlineFormset(
                                             request.POST, request.FILES, 
                                             instance=factura)
        if formset.is_valid():
            form = formset.save(commit=False)
            suma = 0
            for f in form:
                p = producto.get(id=f.producto.pk)
                f.precio = p.precio
                f.sub_total = f.cantidad * p.precio
                suma += f.sub_total
                f.save()
            messages.warning(request, 'Total ' + str(suma))
            return redirect('panaderia:detalle-factura', factura_id=factura.id)
    else:
        formset = DetalleFacturaInlineFormset(instance=factura)
    return render(request, 'panaderia/detalle_factura.html', 
                 {'formset': formset, 'productos': producto})



