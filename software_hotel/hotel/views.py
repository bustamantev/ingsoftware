# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Administrador, Habitacion, Reserva, Tipo_habitacion
from datetime import timedelta, datetime
from .forms import formularioReserva


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
    form = formularioReserva
    data = {'form':form}
    return render(request, "busqueda.html", data)


def resultados(request):
    fecha_actual = datetime.now().date()
    fecha_entrada = None
    fecha_salida = None
    numero_huespedes = None
    tipo_habitacion = None
    if request.method == "POST":
        fecha_entrada = request.POST.get("fecha_entrada")
        fecha_salida = request.POST.get("fecha_salida")
        numero_huespedes = int(request.POST.get("numero_huespedes"))
        tipo_habitacion = int(request.POST.get("tipo_habitacion"))
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
                        "error_fecha_salida": "La fecha de salida no puede ser anterior a la fecha de entrada",
                    })
            if fecha_salida == "":
                fecha_salida = fecha_entrada + timedelta(days=1)
        else:
            fecha_salida = ""
    if request.POST:
        habitaciones_disponibles = Habitacion.objects.all()
        if numero_huespedes != 0:
            habitaciones_disponibles = habitaciones_disponibles.filter(
                capacidad__exact=numero_huespedes)
        if tipo_habitacion != 0:
            habitaciones_disponibles = habitaciones_disponibles.filter(
                tipo_habitacion__exact=tipo_habitacion)
        if fecha_entrada != "" and fecha_salida != "":
            reservas_existen = Reserva.objects.all().filter(
                fecha_entrada__lte=fecha_salida, fecha_salida__gte=fecha_entrada)
            if reservas_existen:
                for i in reservas_existen:
                    habitaciones_disponibles = habitaciones_disponibles.exclude(
                        numero_habitacion__exact=i.habitacion.numero_habitacion)
        print('fecha_actual:',fecha_actual)
        print('fecha_entrada:',fecha_entrada)
        print('fecha_salida:',fecha_salida)
        print('numero_huespedes:',numero_huespedes)
        print('tipo_habitacion:',tipo_habitacion)
        return render(request, "resultados.html", {'habitaciones': habitaciones_disponibles})


def reserva(request):
    return render(request, "resultados.html")


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
