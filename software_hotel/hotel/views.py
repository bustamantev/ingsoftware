# Create your views here.
from django.shortcuts import render, redirect
from functools import wraps
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from .models import Cliente, Administrador, Habitacion, Reserva, Tipo_habitacion, Metodo_pago, Reporte
from datetime import timedelta, datetime
from django.contrib.auth import login, logout, authenticate


def rol_requerido(rol_permiso):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and hasattr(request.user, 'administrador'):
                administrador = request.user.administrador
                if administrador.rol == rol_permiso:
                    return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
        return _wrapped_view
    return decorator



def inicio(request):
    return render(request, "inicio.html")


def busqueda(request):
    return render(request, "busqueda.html")


def resultados(request):
    fecha_actual = datetime.now().date()
    fecha_entrada = None
    fecha_salida = None
    numero_huespedes = None

    if request.method == "POST":

        fecha_entrada = request.POST.get("fecha_entrada")
        fecha_salida = request.POST.get("fecha_salida")
        numero_huespedes = int(request.POST.get("numero_huespedes"))

        if fecha_entrada != "":
            fecha_entrada = datetime.strptime(fecha_entrada, "%Y-%m-%d").date()
            if fecha_entrada < fecha_actual:
                return render(request, "busqueda.html", {
                    "error_fecha_entrada": "La fecha de entrada no puede ser anterior a la fecha actual",
                })
            if fecha_salida != "":
                fecha_salida = datetime.strptime(
                    fecha_salida, "%Y-%m-%d").date()
                if fecha_salida <= fecha_entrada:
                    return render(request, "busqueda.html", {
                        "error_fecha_salida": "La fecha de salida no puede ser anterior o igual a la fecha de entrada",
                    })
            else:
                fecha_salida = fecha_entrada + timedelta(days=1)
        else:
            return render(request, "busqueda.html", {
                "error_fecha_entrada": "debe ingresar una fecha de entrada",
            })
        if numero_huespedes == 0:
            return render(request, "busqueda.html", {
                "error_numero_huesped": "debe ingresar cantidad de personas que se hospedaran",
            })

    if request.method == 'POST':
        habitaciones_disponibles = Habitacion.objects.all()
        habitaciones_disponibles = habitaciones_disponibles.filter(
            capacidad__gte=numero_huespedes)
        reservas_existen = Reserva.objects.all().filter(
            fecha_entrada__lte=fecha_salida, fecha_salida__gte=fecha_entrada)
        if reservas_existen:
            for i in reservas_existen:
                habitaciones_disponibles = habitaciones_disponibles.exclude(
                    numero_habitacion__exact=i.habitacion.numero_habitacion)
        fecha_entrada = datetime.strftime(fecha_entrada, "%d/%m/%Y")
        fecha_salida = datetime.strftime(fecha_salida, "%d/%m/%Y")
        data = {'habitaciones': habitaciones_disponibles,
                'fecha_entrada': fecha_entrada,
                'fecha_salida': fecha_salida,
                'numero_huespedes': numero_huespedes}
        return render(request, "resultados.html", data)


def detalle(request):
    habitacion_id = request.POST.get("habitacion")
    fecha_entrada = request.POST.get("fecha_entrada")
    fecha_salida = request.POST.get("fecha_salida")
    numero_huespedes = request.POST.get("numero_huespedes")

    habitacion = Habitacion.objects.get(habitacion_id=habitacion_id)
    servicios = list(habitacion.tipo_habitacion.servicios.all().values('descripcion'))
    equipos = list(habitacion.tipo_habitacion.equipos.all().values('descripcion'))

    date_in = datetime.strptime(fecha_entrada, '%d/%m/%Y').date()
    date_out = datetime.strptime(fecha_salida, '%d/%m/%Y').date()
    delta_date = (date_out - date_in).days
    precio_final = delta_date * habitacion.precio
    data = {'fecha_entrada': fecha_entrada,
            'fecha_salida': fecha_salida,
            'numero_huespedes': numero_huespedes,
            'habitacion': habitacion,
            'servicios': servicios,
            'equipos': equipos,
            'dias_hospedaje': delta_date,
            'precio_final': precio_final}
    return render(request, "detalle.html", data)

def datos_cliente(request):
    habitacion_id = request.POST.get("habitacion_id")
    fecha_entrada = request.POST.get("fecha_entrada")
    fecha_salida = request.POST.get("fecha_salida")
    numero_huespedes = request.POST.get("numero_huespedes")
    precio_final = request.POST.get("precio_final")
    data = {'habitacion_id':habitacion_id,
    'fecha_entrada':fecha_entrada,
    'fecha_salida':fecha_salida,
    'numero_huespedes':numero_huespedes,
    'precio_final':precio_final,}
    if request.user.is_authenticated:
        correo = request.user.cliente.correo
        data.update({'correo':correo})
        return render(request, 'metodo_pago.html', data)
    else:
        return render(request,'datos_cliente.html', data)


def datos_cliente_done(request):
    if request.method == 'POST':
        habitacion_id = request.POST.get("habitacion_id")
        fecha_entrada = request.POST.get("fecha_entrada")
        fecha_salida = request.POST.get("fecha_salida")
        numero_huespedes = request.POST.get("numero_huespedes")
        precio_final = request.POST.get("precio_final")
        
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        
        flag = True
        data = {'habitacion_id':habitacion_id,
            'fecha_entrada':fecha_entrada,
            'fecha_salida':fecha_salida,
            'numero_huespedes':numero_huespedes,
            'precio_final':precio_final,
            
            'correo':correo,
            'nombre':nombre,
            'apellido':apellido,
            'telefono':telefono}
        if not correo:
            data.update({'error_correo':'Debe ingresar un correo'})
            flag = False

        try:
            cliente = Cliente.objects.get(username = correo)
            use = authenticate(request,username=cliente.username, password='')
            if use is None:
                data.update({'error_correo':'El correo ya se encuentra registrado'})
                flag = False
        except:
            pass
        try:
            administrador = Administrador.objects.get(username=correo)
            data.update({'error_correo':'El correo ya se encuentra registrado'})
            flag = False
        except:
            pass
        if not nombre:
            data.update({'error_nombre':'Debe ingresar un nombre'})
            flag = False
        if not apellido:
            data.update({'error_apellido':'Debe ingresar un apellido'})
        if not telefono: 
            data.update({'error_telefono':'Debe ingresar un numero de telefono'})
            flag = False
        if len(telefono) != 9 or not telefono.isdigit() :
            data.update({'error_telefono':'El telefono ingresado no es valido, debe tener solo 9 digitos.'})
            flag = False
        if not flag:
            return render(request, 'datos_cliente.html', data)
        else:
            return render(request, 'metodo_pago.html', data)




def metodo_pago(request):
    habitacion_id = request.POST.get("habitacion_id")
    fecha_entrada = request.POST.get("fecha_entrada")
    fecha_salida = request.POST.get("fecha_salida")
    numero_huespedes = request.POST.get("numero_huespedes")
    precio_final = request.POST.get("precio_final")

    correo = request.POST.get('correo')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    telefono = request.POST.get('telefono')

    data = {'habitacion_id':habitacion_id,
        'fecha_entrada':fecha_entrada,
        'fecha_salida':fecha_salida,
        'numero_huespedes':numero_huespedes,
        'precio_final':precio_final,
        'correo':correo,
        'nombre':nombre,
        'apellido':apellido,
        'telefono':telefono}
    return render(request, "metodo_pago.html",data)



def realizado(request):
    habitacion_id = request.POST.get("habitacion_id")
    fecha_entrada = request.POST.get("fecha_entrada")
    fecha_salida = request.POST.get("fecha_salida")
    numero_huespedes = request.POST.get("numero_huespedes")
    precio_final = request.POST.get("precio_final")

    correo = request.POST.get('correo')
    nombre = request.POST.get('nombre')
    apellido = request.POST.get('apellido')
    telefono = request.POST.get('telefono')
    if request.method == "POST":
        metodo_pago = int(request.POST.get("metodo_pago"))
        if metodo_pago != 0:
            fecha_entrada = datetime.strptime(fecha_entrada, '%d/%m/%Y').date()
            fecha_salida = datetime.strptime(fecha_salida, '%d/%m/%Y').date()
            numero_huespedes = int(numero_huespedes)
            precio_final = int(precio_final)
            metodo_pago = Metodo_pago.objects.get(pago_id=metodo_pago)
            habitacion = Habitacion.objects.get(habitacion_id=habitacion_id)
            if not request.user.is_authenticated:
                cliente = Cliente(
                    username = correo,
                    correo = correo,
                    nombre = nombre,
                    apellido = apellido,
                    telefono = telefono
                )
                try:
                    cliente = Cliente.objects.get(username = correo)
                    use = authenticate(request,username=cliente.username, password='')
                    if use is None:
                        cliente.set_password('')
                        cliente.save()
                except:
                    cliente.set_password('')
                    cliente.save()
            else:
                cliente = Cliente.objects.get(username=request.user.cliente.username)
            reserva = Reserva(
                fecha_entrada = fecha_entrada,
                fecha_salida = fecha_salida,
                cantidad_personas = numero_huespedes,
                precio_final = precio_final,
                pago = metodo_pago,
                habitacion = habitacion,
                cliente = cliente
            )
            reserva.save()
            return render(request, "realizado.html")
        else:
            return render(request, "metodo_pago.html", {
                "error_metodo_pago": "Debe ingresar un metodo de pago antes de continuar",
            })

def catalogo(request):
    tipos_habitaciones = Tipo_habitacion.objects.all()
    data = []
    for tipo_habitacion in tipos_habitaciones:
        servicios = list(tipo_habitacion.servicios.all().values('descripcion'))
        equipos = list(tipo_habitacion.equipos.all().values('descripcion'))
        data.append({'nombre': tipo_habitacion.nombre,
                    'equipos': equipos,
                    'servicios': servicios})
    return render(request, "catalogo.html", {'tipo_habitacion': data})

def registro_cli(request):
    return render(request, 'registro_cli.html')
    pass

def registro_cli_done(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        vip = request.POST.get('vip')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        flag = True
        data={'correo':correo,
            'nombre':nombre,
            'apellido':apellido,
            'telefono':telefono}
        if not correo:
            data.update({'error_correo':'Debe ingresar un correo'})
            flag = False
        else:
            try:
                cliente = Cliente.objects.get(correo = correo)
                use = authenticate(request,username=cliente.username, password='')
                if use is None:
                    data.update({'error_correo':'El correo ya se encuentra registrado'})
                    flag = False
            except:
                pass
            try:
                administrador = Administrador.objects.get(correo=correo)
                data.update({'error_correo':'El correo ya se encuentra registrado'})
                flag = False
            except:
                pass
        if not nombre:
            data.update({'error_nombre':'Debe ingresar un nombre'})
            flag = False
        if not apellido:
            data.update({'error_apellido':'Debe ingresar un apellido'})
        if not telefono: 
            data.update({'error_telefono':'Debe ingresar un numero de telefono'})
            flag = False
        if len(telefono) != 9 or not telefono.isdigit() :
            data.update({'error_telefono':'El telefono ingresado no es valido, debe tener solo 9 digitos.'})
            flag = False
        if not vip:
            vip = False
        else:
            vip = True
        if not password:
            data.update({'error_password':'Debe ingresar una contraseña'})
            flag = False
        else:
            if not password2:
                data.update({'error_password':'Debe ingresar repetir contraseña'})
                flag = False
            else:
                if password != password2:
                    data.update({'error_password':'Las contraseñas no coinciden'})
                    flag = False
        if not flag:
            return render(request, 'registro_cli.html', data)
        else:
            try:
                cliente = Cliente.objects.get(correo = correo)
                use = authenticate(request,username=cliente.username, password='')
                if use is None:
                    cliente = Cliente(username = correo,
                                    correo = correo,
                                    nombre = nombre,
                                    apellido = apellido,
                                    telefono = telefono,
                                    vip = vip)
                else:
                    cliente.username = correo
                    cliente.correo = correo
                    cliente.nombre = nombre
                    cliente.apellido = apellido
                    cliente.telefono = telefono
                    cliente.vip = vip
            except:
                cliente = Cliente(username = correo,
                    correo = correo,
                    nombre = nombre,
                    apellido = apellido,
                    telefono = telefono,
                    vip = vip)
            cliente.set_password(password)
            cliente.save()
            login(request, cliente)
            return redirect('inicio')

def iniciar_sesion_cli(request):
    return render(request, 'iniciar_sesion_cli.html')

def iniciar_sesion_cli_done(request):
    if request.method == 'POST':
        username = request.POST.get('correo')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            data = {'correo': username,
                    'error': 'Correo y/o contraseña invalidos'}
            return render(request, 'iniciar_sesion_cli.html', data)


def cerrar_sesion_cli(request):
    logout(request)
    return redirect('inicio')


#ADMINISTRACION
def inicio_sesion_adm(request):
    return render(request,'administracion/inicio_sesion_adm.html')

def inicio_sesion_adm_done(request):
    if request.method == 'POST':
        username = request.POST.get('correo')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        data = {'correo': username,}
        if user is not None:
            login(request, user)
        else:
            data.update({'error':'Usuario y/o contraseña invalidos.'})
            return render(request, 'administracion/inicio_sesion_adm.html', data)
        return redirect('menu_adm')

@login_required
def cerrar_sesion_adm(request):
    logout(request)
    return redirect('inicio_sesion_adm')

def registrarse_adm(request):
    return render(request,'administracion/registrarse_adm.html')

def registrarse_adm_done(request):
    if request.method == 'POST':
        correo = request.POST.get('correo')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono')
        rol = request.POST.get('rol')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        data = {
            'correo':correo,
            'nombre':nombre,
            'apellido':apellido,
            'telefono':telefono,
        }
        if correo:
            try:
                Administrador.objects.get(correo = correo)
                data.update({'error_email':'El correo ingresado ya esta registrado'})
                return render(request,'administracion/registrarse_adm.html', data)
            except:
                pass
        else:
            data.update({'error_email':'El correo no puede quedar vacio'})
            return render(request,'administracion/registrarse_adm.html', data)
        if not nombre:
            data.update({'error_nombre':'El nombre no puede quedar vacio'})
            return render(request,'administracion/registrarse_adm.html', data)
        if not apellido:
            data.update({'error_apellido':'El apellido no puede quedar vacio'})
            return render(request,'administracion/registrarse_adm.html', data)
        if not telefono:
            data.update({'error_telefono':'El telefono no puede quedar vacio'})
            return render(request,'administracion/registrarse_adm.html', data)
        else:
            try:
                telefono = int(telefono)
                if len(str(telefono)) != 9:
                    data.update({'error_telefono':'El telefono tiene que tener 9 digitos'})
                    return render(request,'administracion/registrarse_adm.html', data)
            except:
                data.update({'error_telefono':'El telefono ingresado no es valido, solo puede ingresar numeros'})
                return render(request,'administracion/registrarse_adm.html', data)
        if not rol:
            data.update({'error_rol':'Debe seleccionar un rol para el usuario'})
            return render(request,'administracion/registrarse_adm.html', data)
        if not password:
            data.update({'error_password':'Debe ingresar una contraseña'})
            return render(request,'administracion/registrarse_adm.html', data)
        else:
            if not password2:
                data.update({'error_password':'Debe ingresar repetir contraseña'})
                return render(request,'administracion/registrarse_adm.html', data)
            else:
                if password != password2:
                    data.update({'error_password':'Las contraseñas no coinciden'})
                    return render(request,'administracion/registrarse_adm.html', data)
        administrador = Administrador(
            username = correo,
            correo = correo,
            nombre = nombre,
            apellido = apellido,
            telefono = telefono,
            rol = rol,
        )
        administrador.set_password(password)
        administrador.save()
        login(request,administrador)
    return redirect('menu_adm')



@login_required
def menu_adm(request):
    return render(request, 'administracion/menu_adm.html')

@login_required
def reporte(request):
    if request.method == 'POST':
        reporte = request.POST.get('reporte')
        if reporte:
            reporte = Reporte(
                reporte = reporte,
                administrador = Administrador.objects.get(username=request.user)
            )
            reporte.save()
            return redirect('menu_adm')
        else:
            return render(request, 'administracion/reporte.html', {'error':'El campo no puede quedar vacio, debe ingresar un reporte.'})
    else:
        return render(request, 'administracion/reporte.html')

def reporte_done(request):
    return redirect('menu_adm')


@login_required
def modificar_habitacion_adm(request):
    habitaciones = Habitacion.objects.all()
    data={'lista_habitaciones':habitaciones}
    return render(request, 'administracion/modificar_habitacion_adm.html', data)

def modificar_habitacion_adm_done(request):
    if request.method == 'POST':
        habitacion_id = request.POST.get('habitacion_id')
        precio = request.POST.get('precio')
        if not precio:
            return redirect('modificar_habitacion_adm')
        else:
            precio = int(precio)
            habitacion_id = int(habitacion_id)
            habitacion = Habitacion.objects.get(habitacion_id=habitacion_id)
            habitacion.precio=precio
            habitacion.save()
            return redirect('modificar_habitacion_adm')

@login_required
def listar_reportes(request):
    reportes = Reporte.objects.all()
    data = {'reportes':reportes}
    return render(request,'administracion/listar_reportes.html', data)

@login_required
def ver_reporte(request):
    if request.method == 'POST':
        reporte_id = request.POST.get('reporte_id')
        reporte = Reporte.objects.get(reporte_id = reporte_id)
        data = {'reporte_id': reporte.reporte_id,
                'reporte': reporte.reporte,
                'administrador':reporte.administrador}
        return render(request, 'administracion/ver_reporte.html', data)

@login_required
def lista_reserva(request):
    reservas = Reserva.objects.all()
    data = {'reservas': reservas}
    return render(request, 'administracion/lista_reserva.html', data)

@login_required
def editar_reserva(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        reserva = Reserva.objects.get(reserva_id = reserva_id)
        fecha_entrada = datetime.strftime(reserva.fecha_entrada, "%Y-%m-%d")
        fecha_salida = datetime.strftime(reserva.fecha_salida, "%Y-%m-%d")
        habitaciones = Habitacion.objects.all()
        clientes = Cliente.objects.all()
        data = {'reserva': reserva,
                'fecha_entrada':fecha_entrada,
                'fecha_salida':fecha_salida,
                'habitaciones':habitaciones,
                'clientes':clientes}
    return render(request, 'administracion/editar_reserva.html', data)

def editar_reserva_done(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        fecha_entrada = request.POST.get('fecha_entrada')
        fecha_salida = request.POST.get('fecha_salida')
        cantidad_personas = request.POST.get('cantidad_personas')
        numero_habitacion = request.POST.get('numero_habitacion')
        precio_final = request.POST.get('precio_final')
        correo_cliente = request.POST.get('correo')
        
        reserva = Reserva.objects.get(reserva_id = reserva_id)
        habitacion = Habitacion.objects.get(numero_habitacion = numero_habitacion)
        cliente = Cliente.objects.get(username = correo_cliente)
        
        reserva.fecha_entrada = fecha_entrada
        reserva.fecha_salida = fecha_salida
        reserva.cantidad_personas = cantidad_personas
        reserva.habitacion = habitacion
        reserva.precio_final = precio_final
        reserva.cliente = cliente
        
        reserva.save()
        return redirect('lista_reserva')

def eliminar_reserva_done(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        reserva = Reserva.objects.get(reserva_id = reserva_id)
        reserva.delete()
        return redirect('lista_reserva')

@login_required
def listar_reserva_equipos(request):
    reservas = Reserva.objects.all()
    data = {'reservas':reservas}
    return render(request, 'administracion/listar_reserva_equipos.html', data)


def ver_reserva_equipo(request):
    if request.method == 'POST':
        reserva_id = request.POST.get('reserva_id')
        reserva = Reserva.objects.get(reserva_id = reserva_id)
        servicios = list(reserva.habitacion.tipo_habitacion.servicios.all().values('descripcion'))
        equipos = list(reserva.habitacion.tipo_habitacion.equipos.all().values('descripcion'))

        data = {'reserva':reserva,
                'servicios':servicios,
                'equipos':equipos}
        return render(request, 'administracion/ver_reserva_equipo.html', data)
    pass
