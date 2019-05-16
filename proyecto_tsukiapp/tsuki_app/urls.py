from django.urls import path
from . import views

app_name = 'tsuki_app'

urlpatterns = [
    # en este path se van a ver todos los pedidos del dia
    path('',views.pedidos,name='pedidos'),
    # en este path se van a crear un nuevo pedido
    path('nuevopedido/',views.empezarpedido,name='empezarpedido'),
    path('nuevopedido/<slug:producto>/',views.incorporandoitems,name='incorporando'),
    path('eliminarproducto/<slug:productoaeliminar>/',views.eliminarproducto,name='eliminarproducto'),
    path('confirmarpedido/',views.confirmarpedido ,name='confirmarpedido'),
    path('modificarpedido/<int:pk>/',views.modificarpedido ,name='modificarpedido'),
    path('modificarpedido/agregar/<int:pk_pedido>/<slug:pk_item>/',views.modificarpedido_agregar ,name='agregarproducto'),
    path('modificarpedido/quitar/<int:pk_pedido>/<slug:pk_item>/',views.modificarpedido_quitar ,name='quitarproducto'),
    path('<int:pk>/',views.pedidos,name='eliminarpedido'),
    path('<int:day>/<int:month>/<int:year>/',views.filtrarfecha,name='filtrarporfecha'),
    path('producciondeldia',views.producciondeldia,name='producciondiaria'),
#     #asi se asocian las CreatViews.as_view(),name='create'),
#     #si voy a update y al nombre de la pk de la escuela
#     path('update/<int:pk>/',views.SchoolUpdateView.as_view(),name='update'),
#     path('delete/<int:pk>/',views.SchoolDeleteView.as_view(),name='delete')
 ]
