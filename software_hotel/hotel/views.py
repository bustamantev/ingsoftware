# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Administrador, Habitacion, Reserva, Tipo_habitacion, Metodo_pago
from datetime import timedelta, datetime, date


def cliente_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and isinstance(request.user, Cliente):
            return view_func(request, *args, **kwargs)
        else:
            raise Http404("Página no encontrada")
    return _wrapped_view


def administrador_required(role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and isinstance(request.user, Administrador) and request.user.role == role:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404("Página no encontrada")
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

    if request.POST:
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
    servicios = list(
        habitacion.tipo_habitacion.servicios.all().values('descripcion'))
    equipos = list(
        habitacion.tipo_habitacion.equipos.all().values('descripcion'))

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


def metodo_pago(request):
    habitacion_id = request.POST.get("habitacion_id")
    fecha_entrada = request.POST.get("fecha_entrada")
    fecha_salida = request.POST.get("fecha_salida")
    numero_huespedes = request.POST.get("numero_huespedes")
    precio_final = request.POST.get("precio_final")
    data = {'habitacion_id':habitacion_id,
            'fecha_entrada':fecha_entrada,
            'fecha_salida':fecha_salida,
            'numero_huespedes':numero_huespedes,
            'precio_final':precio_final
            }
    return render(request, "metodo_pago.html",data)


def realizado(request):
    habitacion_id = request.POST.get("habitacion_id")
    fecha_entrada = request.POST.get("fecha_entrada")
    fecha_salida = request.POST.get("fecha_salida")
    numero_huespedes = request.POST.get("numero_huespedes")
    precio_final = request.POST.get("precio_final")
    if request.method == "POST":
        metodo_pago = int(request.POST.get("metodo_pago"))
        if metodo_pago != 0:
            fecha_entrada = datetime.strptime(fecha_entrada, '%d/%m/%Y').date()
            fecha_salida = datetime.strptime(fecha_salida, '%d/%m/%Y').date()
            numero_huespedes = int(numero_huespedes)
            precio_final = int(precio_final)
            metodo_pago = Metodo_pago.objects.get(pago_id=metodo_pago)
            habitacion = Habitacion.objects.get(habitacion_id=habitacion_id)
            
            reserva = Reserva(
                fecha_entrada = fecha_entrada,
                fecha_salida = fecha_salida,
                cantidad_personas = numero_huespedes,
                precio_final = precio_final,
                pago = metodo_pago,
                habitacion = habitacion
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


@login_required
@cliente_required
def vista_perfil_cliente(request):
    # Lógica para que los clientes reserven habitaciones
    pass


@login_required
@administrador_required('TI')
def vista_administrador_admin(request):
    # Lógica para la vista de administrador con rol 'admin'
    pass


@login_required
@administrador_required('Administrador de hotel')
def vista_administrador_supervisor(request):
    # Lógica para la vista de administrador con rol 'supervisor'
    pass
