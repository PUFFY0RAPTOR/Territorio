from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Aprendiz, Monitoria, Actividades, Usuario
from django.urls import reverse
from django.db import IntegrityError #Gestión de errorees de bases de datos

#Mensajes tipo cookies temporales
from django.contrib import messages

#Para la paginación
from django.core.paginator import Paginator

#Para poder filtrar más datos
from django.db.models import Q

#El request es un parametro que necesita django para manipular la peticion-respuesta (GET, POST, DELETE)

def index(request):    
    return render(request, 'territorio/index.html')


def loginFormulario(request):
    return render(request, 'territorio/login/login.html')


def login(request):
    if request.method == "POST":
        try:
            #Capturar datos del formulario
            user = request.POST["usuario"]
            passw = request.POST["clave"]

            #Verificar si existe en base de datos, la ',' es el operador lógico Y.
            q = Usuario.objects.get(usuario = user, password = passw)

            #Crear la variable de sesión
            request.session['auth'] = [q.id, q.nombre, q.apellido, q.usuario, q.rol, q.get_rol_display()]

            return redirect('territorio:index')

        except Usuario.DoesNotExist:
            messages.error(request, "Usuario o contraseña incorrectos...")
            return redirect('territorio:loginForm')
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('territorio:loginForm')


def logout(request):
    try:
        del request.session['auth']
        messages.success(request, 'Sesión cerrada correctamente')

    except Exception as e:
        messages.error(request, f"Ocurrió un error, intente de nuevo...")
    
    return redirect('territorio:index')

#------------------------------------------- Aprendices -----------------------------------------------------

#Hacer un decorador para el control de autenticación
def listarAprendiz(request):

    auth = request.session.get('auth', False)
    if auth and (auth[4] == 'R' or auth[4] == 'I'):
        q = Aprendiz.objects.all()

        #Paginación
        pag = Paginator(q, 6)
        page_number = request.GET.get('page') #Obtiene variables de la URL

        #Sobreescibe el query
        q = pag.get_page(page_number)

        contexto = { 'page_obj': q }

        return render(request, 'territorio/aprendiz/listar_aprendiz.html', contexto)
    else:
        messages.warning(request, 'Usted no ha iniciado sesión...')
        return redirect('territorio:loginForm')


def listarAprendizBuscar(request):

    if request.method == "POST":

        #Se filtra para poder encontrar dependiendo de lo que se busque
        q = Aprendiz.objects.filter(
            Q(cedula__icontains = request.POST["dato_buscar"]) |
            Q(nombre__icontains = request.POST["dato_buscar"]) |
            Q(apellido__icontains = request.POST["dato_buscar"]) 
        )

        #Paginación
        pag = Paginator(q, 6)
        page_number = request.GET.get('page') #Obtiene variables de la URL

        #Sobreescibe el query
        q = pag.get_page(page_number)

        contexto = { 'page_obj': q, 'dato_buscado':  request.POST["dato_buscar"]}

        return render(request, 'territorio/aprendiz/listar_aprendiz_ajax.html', contexto)
    else:
        return redirect('territorio:aprendices')


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
            messages.success(request, 'Aprendiz guardado correctamente')
            return redirect('territorio:aprendices')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:aprendices')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:aprendices')
        #return HttpResponse("Error : " + str(e))


#------------------------------------------- Monitorias -----------------------------------------------------


def listarMonitorias(request):

    m = Monitoria.objects.all()

    pag = Paginator(m, 3)
    page_number = request.GET.get('page')

    m = pag.get_page(page_number)

    contexto = { 'datos': m}

    return render(request, 'territorio/monitoria/listar_monitoria.html', contexto)

('cat', 'aprendiz', 'fecha_inicio', 'fecha_final', )

def listarMonitoriasBuscar(request):
    if request.method == "POST":
        q = Monitoria.objects.filter(
            Q(cat__icontains = request.POST["dato_buscar"]) |
            Q(aprendiz__icontains = Aprendiz.objects.get(pk = request.POST["dato_buscar"])) |
            Q(fecha_inicio__icontains = request.POST["dato_buscar"]) |
            Q(fecha_final__icontains = request.POST["dato_buscar"]) 
        )

        pag = Paginator(q, 4)
        pag_number = request.GET.get("page")

        # q = 

    else: 
        pass


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
            
            a.cat = request.POST["cat"]
            a.aprendiz = Aprendiz.objects.get(pk = request.POST["aprendiz"])
            a.fecha_inicio = request.POST["fecha_inicio"]
            a.fecha_final = request.POST["fecha_final"]

            a.save()
            messages.success(request, 'Monitoria guardada correctamente')
            return redirect('territorio:monitorias')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:monitorias')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:monitorias')


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


#------------------------------------------- Actividades -----------------------------------------------------


def listarActividades(request):

    a = Actividades.objects.all()
    contexto = {'datos': a}

    return render(request, 'territorio/actividades/listar_actividades.html', contexto)


#------------------------------------------- Usuarios -----------------------------------------------------
def listarUsuario(request):

    auth = request.session.get('auth', False)
    if auth and (auth[4] == 'R' or auth[4] == 'I'):
        q = Usuario.objects.all()

        #Paginación
        pag = Paginator(q, 6)
        page_number = request.GET.get('page') #Obtiene variables de la URL

        #Sobreescibe el query
        q = pag.get_page(page_number)

        contexto = { 'page_obj': q }

        return render(request, 'territorio/usuario/listarUsuario.html', contexto)
    else:
        messages.warning(request, 'Usted no ha iniciado sesión...')
        return redirect('territorio:loginForm')

""" def listarAprendizBuscar(request):

    if request.method == "POST":

        #Se filtra para poder encontrar dependiendo de lo que se busque
        q = Aprendiz.objects.filter(
            Q(cedula__icontains = request.POST["dato_buscar"]) |
            Q(nombre__icontains = request.POST["dato_buscar"]) |
            Q(apellido__icontains = request.POST["dato_buscar"]) 
        )

        #Paginación
        pag = Paginator(q, 6)
        page_number = request.GET.get('page') #Obtiene variables de la URL

        #Sobreescibe el query
        q = pag.get_page(page_number)

        contexto = { 'page_obj': q, 'dato_buscado':  request.POST["dato_buscar"]}

        return render(request, 'territorio/aprendiz/listar_aprendiz_ajax.html', contexto)
    else:
        return redirect('territorio:aprendices') """


def eliminarUsuario(request, id):
    try:
        a = Usuario.objects.get(pk = id) 
        a.delete()
        return HttpResponseRedirect(reverse('territorio:usuarios'))

    except Aprendiz.DoesNotExist:
        return HttpResponse('Error: Aprendiz no existe')
    except IntegrityError:
        return HttpResponse('Error: No se puede eliminar al Aprendiz ya que está siendo usado')
    except Exception as e:
        return HttpResponse(f'Error: {e}')      


def usuFormularioEditar(request, id):
    a = Usuario.objects.get(pk = id)
    q = Usuario.objects.all()
    contexto = {'datos': a, 'usu':q}

    return render(request, 'territorio/usuario/editarUsuario.html', contexto) 


def actualizarUsuario(request):
    try:
        if request.method == "POST":
            a = Usuario.objects.get(pk = request.POST["id"])
            
            nombre = request.POST["nombre"]
            apellido = request.POST["apellido"]
            correo = request.POST["correo"]
            password = request.POST["passw"]
            rol = request.POST["roles"]
            foto = request.POST["foto"]

            a.save()
            messages.success(request, 'Usuario guardado correctamente')
            return redirect('territorio:usuarios')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:usuarios')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:usuarios')


def usuFormulario(request):

    q = Usuario.objects.all()

    contexto = {'usu': q}

    return render(request, 'territorio/usuario/crearUsuario.html', contexto)


def usuGuardar(request):
    try:
        if request.method == "POST":
            q = Usuario(
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                correo = request.POST["correo"],
                password = request.POST["passw"],
                rol = request.POST["roles"],
                foto = request.POST["foto"],
            )
            q.save()
            messages.success(request, 'Usuario guardado correctamente')
            return redirect('territorio:usuarios')
            #return HttpResponseRedirect(reverse('territorio:aprendices'))
        else:
            messages.warning(request, 'A hackear a su madre perr*')
            return redirect('territorio:usuarios')    
    except Exception as e:
        messages.error(request, 'Error : ' + str(e))
        return redirect('territorio:usuarios')


#Consultar offcanvas en Bootstrap 5