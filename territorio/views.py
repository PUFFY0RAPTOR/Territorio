from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Aprendiz, Monitoria, Actividades
from django.urls import reverse
from django.db import IntegrityError #Gestión de errorees de bases de datos

#Mensajes tipo cookies temporales
from django.contrib import messages

#Para la paginación
from django.core.paginator import Paginator


#El request es un parametro que necesita django para manipular la peticion-respuesta (GET, POST, DELETE)

def index(request):    
    return render(request, 'territorio/index.html')


def listarAprendiz(request):

    q = Aprendiz.objects.all()

    #Paginación
    pag = Paginator(q, 6)
    page_number = request.GET.get('page')

    #Sobreescibe el query
    q = pag.get_page(page_number)

    contexto = { 'page_obj': q }

    return render(request, 'territorio/aprendiz/listar_aprendiz.html', contexto)


def eliminarAprendiz(request, id):
    try:
        a = Aprendiz.objects.get(pk = id) 
        a.delete()
        return HttpResponseRedirect(reverse('territorio:aprendices'))

    except Aprendiz.DoesNotExist:
        return HttpResponse('Error: Aprendiz no existe')
    except IntegrityError:
        return HttpResponse('Error: No se puede eliminar al Aprendiz ya que está siendo usado')
    except Exception as e:
        return HttpResponse(f'Error: {e}')      


def aprendizFormularioEditar(request, id):
    a = Aprendiz.objects.get(pk = id)
    contexto = {'datos': a}

    return render(request, 'territorio/aprendiz/editar_aprendiz.html', contexto) 


def actualizarAprendiz(request):
    try:
        if request.method == "POST":
            a = Aprendiz.objects.get(pk = request.POST["cedula"])
            
            a.cedula = request.POST["cedula"]
            a.nombre = request.POST["nombre"]
            a.apellido = request.POST["apellido"]
            a.fecha_nacimiento = request.POST["fecha_nacimiento"]

            a.save()
            messages.success(request, 'Aprendiz guardado correctamente')
            return redirect('territorio:aprendices')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:aprendices')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:aprendices')


def aprendicesFormulario(request):
    return render(request, 'territorio/aprendiz/crear_aprendiz.html')


def aprendicesGuardar(request):
    try:
        if request.method == "POST":
            q = Aprendiz(
                cedula = request.POST["cedula"],
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                fecha_nacimiento = request.POST["fecha_nacimiento"],
            )
            q.save()
            messages.warning(request, 'Aprendiz guardado correctamente')
            return redirect('territorio:aprendices')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:aprendices')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:aprendices')
        #return HttpResponse("Error : " + str(e))

#------------------------------------------- Aprendices -----------------------------------------------------


def listarMonitorias(request):

    m = Monitoria.objects.all()

    contexto = { 'datos': m}

    return render(request, 'territorio/monitoria/listar_monitoria.html', contexto)


def monitoriaFormulario(request):

    q = Aprendiz.objects.all()

    #s = Monitoria.objects.get()

    contexto = { 'data': q}

    return render(request, 'territorio/monitoria/crear_monitoria.html', contexto)


def monitoriaFormularioEditar(request, id):

    a = Monitoria.objects.get(pk = id)
    p = Aprendiz.objects.all()

    contexto = {'datos': a, 'aprendices': p}

    return render(request, 'territorio/monitoria/editar_monitoria.html', contexto) 


def eliminarMonitoria(request, id):
    try:
        a = Monitoria.objects.get(pk = id) 
        a.delete()
        return HttpResponseRedirect(reverse('territorio:monitorias'))

    except Aprendiz.DoesNotExist:
        return HttpResponse('Error: Aprendiz no existe')
    except IntegrityError:
        return HttpResponse('Error: No se puede eliminar al Aprendiz ya que está siendo usado')
    except Exception as e:
        return HttpResponse(f'Error: {e}')


def actualizarMonitoria(request):
    try:
        if request.method == "POST":
            a = Monitoria.objects.get(pk = request.POST["id"])
            
            a.cedula = request.POST["cedula"]
            a.nombre = request.POST["nombre"]
            a.apellido = request.POST["apellido"]
            a.fecha_nacimiento = request.POST["fecha_nacimiento"]

            a.save()
            messages.success(request, 'Aprendiz guardado correctamente')
            return redirect('territorio:aprendices')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:aprendices')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:aprendices')


def monitoriaGuardar(request):
    
    f = request.POST["aprendiz"]
    
    try:
        q = Monitoria(
            cat = request.POST["cat"],
            aprendiz = Aprendiz.objects.get(pk = f),
            fecha_inicio = request.POST["fecha_inicio"],
            fecha_final = request.POST["fecha_final"],
        )
        q.save()
        return HttpResponseRedirect(reverse('territorio:monitorias'))

    except Exception as e:
        return HttpResponse("Error : " + str(e))


#------------------------------------------- Monitorias -----------------------------------------------------


def listarActividades(request):

    a = Actividades.objects.all()
    contexto = {'datos': a}

    return render(request, 'territorio/actividades/listar_actividades.html', contexto)


#------------------------------------------- Actividades -----------------------------------------------------



#Consultar offcanvas en Bootstrap 5