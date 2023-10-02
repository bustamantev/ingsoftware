from django.contrib import admin
from .models import Equipo, Servicio, Hotel, Metodo_pago, Tipo_habitacion, Habitacion, Administrador, Cliente, Reserva, Reporte

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)

@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'direccion',)

@admin.register(Metodo_pago)
class Metodo_pagoAdmin(admin.ModelAdmin):
    list_display = ('descripcion',)

@admin.register(Tipo_habitacion)
class Tipo_habitacionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

@admin.register(Habitacion)
class HabitacionAdmin(admin.ModelAdmin):
    list_display = (
        'numero_habitacion', 'metros_cuadrados', 'precio',
        'tipo_habitacion', 'hotel',
    )

@admin.register(Administrador)
class AdministradorAdmin(admin.ModelAdmin):
    list_display = ('correo', 'nombre', 'apellido', 'rol')

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('correo', 'nombre', 'apellido', 'telefono', 'vip')

@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = (
        'fecha_entrada', 'fecha_salida', 'cantidad_personas', 'precio_final',
        'fecha_hora_pago', 'cliente', 'pago', 'habitacion',
    )

@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = (
        'reporte','administrador'
    )
