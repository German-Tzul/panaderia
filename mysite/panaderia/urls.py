from django.urls import path


from .import views


app_name = 'panaderia'


urlpatterns = [
    # 1
    path('', views.index, name='index'),
    path('inventario/', views.InventarioProductoListView.as_view(), name='inventario'),
    path('<int:pk>/producto/', views.DetalleComprasDetailView.as_view(), name='producto'),
    path('compras/', views.ComprasCreateView.as_view(), name='compras'),
    path('<int:compras_id>/detalle/compras/', views.detalle_compras, name='detalle-compras'),
    path('producto/utilizado', views.ProductoUtilizadoView.as_view(), name='producto-utilizado'),
    # 6
    path('factura/', views.FacturaCreateView.as_view(), name='factura'),
    # 7
    path('<int:factura_id>/detalle/factura/', views.detalle_factura, name='detalle-factura'),




]
