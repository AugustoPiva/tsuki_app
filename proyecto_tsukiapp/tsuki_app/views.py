from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from .models import Pedidos,Listaprecios,Productosordenados
from .forms import FormularioNuevoPedido,Fecha
from django.views.generic import (View,TemplateView,
                                ListView,DetailView,
                                CreateView,DeleteView,
                                UpdateView)
from datetime import datetime,date
import json
from django.shortcuts import redirect
global carrito
carrito={}
#si queres usar template views
# class PruebaTemplateView(TemplateView):
#     template_name = 'algo.html
#
#     def get_context_data(self, **kwargs):
#         context= super().get_context_data(**kwargs)
#         context['injectme']= 'BASIC INJECTION'
#         return context
#
def pedidos(request,**kwargs):
    try:
        Pedidos.objects.get(id=kwargs['pk']).delete()
    except:
        pass

    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=date.today().day,
                                                            pedido__fecha__month=date.today().month,
                                                            pedido__fecha__year=date.today().year)
        # listadepedidos=Pedidos.objects.filter(fecha__day=date.today().day)
    if request.method == "POST":

        day   = int(request.POST['dia'][8:10])
        month = int(request.POST['dia'][5:7])
        year  = int(request.POST['dia'][0:4])

        return HttpResponseRedirect(reverse('tsuki_app:filtrarporfecha',args=(day,month,year)))

    # productosdelasordenes=Productosordenados.objects.all()
    carrito.clear()
    x=date.today()
    fecha=Fecha({'dia':x})

    return render(request,'tsuki_app/pedidos_list.html',{'x':x,'fecha':fecha,'productosdeordenes':productosdelasordenes})

def filtrarfecha(request,**kwargs):

    x= datetime(kwargs['year'],kwargs['month'],kwargs['day'])
    fecha=Fecha({'dia':x})
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=kwargs['day'],
                                                            pedido__fecha__month=kwargs['month'],
                                                            pedido__fecha__year=kwargs['year'])

    if request.method == "POST":
        day   = int(request.POST['dia'][8:10])
        month = int(request.POST['dia'][5:7])
        year  = int(request.POST['dia'][0:4])

        return HttpResponseRedirect(reverse('tsuki_app:filtrarporfecha',args=(day,month,year)))

    carrito.clear()
    return render(request,'tsuki_app/pedidos_list.html',{'x':x,'fecha':fecha,'productosdeordenes':productosdelasordenes})

def Index(request):
    return render(request, 'tsuki_app/base.html',{})

def empezarpedido(request):

    productos= Listaprecios.objects.all()
    return render(request,'tsuki_app/nuevo_pedido.html',{'lista':productos,'carro':carrito})

def incorporandoitems(request,producto):

    productos= Listaprecios.objects.all()

    if producto in carrito:
        carrito[producto]= carrito[producto] +  1

    else:
        carrito[producto]=1

    return render(request,'tsuki_app/nuevo_pedido.html',{'lista':productos,'carro':carrito})
        # carrito[producto]=carrito[producto]+1

def eliminarproducto(request,productoaeliminar):

    productos= Listaprecios.objects.all()
    if carrito[productoaeliminar] == 1:
        del carrito[productoaeliminar]
    else:
        carrito[productoaeliminar] = carrito[productoaeliminar]-1

    return render(request,'tsuki_app/nuevo_pedido.html',{'lista':productos,'carro':carrito})

def modificarpedido(request,pk):
    productos= Listaprecios.objects.all()
    orden=Pedidos.objects.get(id=pk)
    carrito=Productosordenados.objects.filter(pedido=pk)

    return render(request,'tsuki_app/modificar_pedido.html',{'lista':productos,'carro':carrito,'orden':orden})

def modificarpedido_quitar(request,pk_pedido,pk_item):
    Productosordenados.objects.get(id=pk_item).delete()
    productos= Listaprecios.objects.all()
    orden=Pedidos.objects.get(id=pk_pedido)
    carrito=Productosordenados.objects.filter(pedido=pk_pedido)

    return render(request,'tsuki_app/modificar_pedido.html',{'lista':productos,'carro':carrito,'orden':orden})

def modificarpedido_agregar(request,pk_pedido,pk_item):
    carrito=Productosordenados.objects.filter(pedido=pk_pedido)
    orden=Pedidos.objects.get(id=pk_pedido)
    try:
        product = carrito.get(item=pk_item)
        product.cantidad += 1
        product.save()
    except:
        itemagregar= Listaprecios.objects.get(id=pk_item)
        product = Productosordenados.objects.create(item=itemagregar, pedido=orden)
        product.save()

    productos= Listaprecios.objects.all()
    carrito=Productosordenados.objects.filter(pedido=pk_pedido)

    return render(request,'tsuki_app/modificar_pedido.html',{'lista':productos,'carro':carrito,'orden':orden})

def confirmarpedido(request):

    form = FormularioNuevoPedido(request.POST or None)
    a= Listaprecios.objects.all()
    pedidos= Pedidos.objects.all()

    if request.method == "POST" and form.is_valid():
        form.save()
        ultid= Pedidos.objects.latest('id')
        ultimopedido= Pedidos.objects.get(id=ultid.id)

        for i in carrito:
                prod=get_object_or_404(Listaprecios,id=i)
                order_item = Productosordenados.objects.create(item=prod, cantidad=carrito[i],pedido=ultimopedido)
                order_item.save()

        return HttpResponseRedirect('/tsuki_app/')
    else:
        return render(request, 'tsuki_app/confirmar_pedido.html',{'lista':a,'form':form, 'carro':carrito})

    return render(request,'tsuki_app/confirmar_pedido.html',{'lista':a,'form':form, 'carro':carrito})

def producciondeldia(request,**kwargs):
    productosdelasordenes=Productosordenados.objects.filter(pedido__fecha__day=date.today().day,
                                                            pedido__fecha__month=date.today().month,
                                                            pedido__fecha__year=date.today().year)

    return render(request,'tsuki_app/producciondiaria.html',{'productosdelasordenes':productosdelasordenes})
