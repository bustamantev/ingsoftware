from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone


class Equipo(models.Model):
    equipo_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.descripcion


class Servicio(models.Model):
    servicio_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return self.descripcion


class Hotel(models.Model):
    hotel_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200, null=False, blank=False)
    direccion = models.TextField(max_length=500, null=False, blank=False)

    def __str__(self):
        return self.nombre


class Metodo_pago(models.Model):
    pago_id = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=100)

    def __str__(self):
        return self.descripcion


class Tipo_habitacion(models.Model):
    tipo_habitacion_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    equipos = models.ManyToManyField(Equipo)
    servicios = models.ManyToManyField(Servicio)
    def __str__(self):
        return self.nombre
    

class Habitacion(models.Model):
    habitacion_id = models.AutoField(primary_key=True)
    disponibilidad = models.BooleanField(null=False, blank=False)
    numero_habitacion = models.IntegerField(null=False, blank=False)
    capacidad = models.IntegerField(null=False, blank=False)
    metros_cuadrados = models.IntegerField(null=False, blank=False)
    precio = models.IntegerField(null=False, blank=False)
    tipo_habitacion = models.ForeignKey(
        Tipo_habitacion, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)

    def __str__(self):
        return f'Habitación {self.numero_habitacion} en {self.hotel.nombre}'


class Administrador(AbstractUser):
    ROLES = (
        ('TI', 'TI'),
        ('Administrador de hotel', 'Administrador de hotel'),
        ('Administrador de reserva', 'Administrador de reserva'),
        ('Empleado', 'Empleado'),
    )
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    telefono = models.IntegerField(null=False, blank=False)
    role = models.CharField(max_length=24, choices=ROLES,
                            default='Administrador de hotel')
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(
        Group,
        related_name="administradores",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="administradores",
    )

    def __str__(self):
        return self.email


class Cliente(AbstractUser):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=50, null=False, blank=False)
    apellido = models.CharField(max_length=50, null=False, blank=False)
    telefono = models.IntegerField(null=False, blank=False)
    vip = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(
        Group,
        related_name="clientes",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="clientes",
    )

    def __str__(self):
        return self.email


class Reserva(models.Model):
    reserva_id = models.AutoField(primary_key=True)
    fecha_entrada = models.DateField()
    fecha_salida = models.DateField()
    cantidad_personas = models.IntegerField(null=False)
    precio_final = models.IntegerField()
    fecha_hora_pago = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(
        Cliente, on_delete=models.CASCADE, null=True, blank=True)
    pago = models.ForeignKey(Metodo_pago, on_delete=models.CASCADE)
    habitacion = models.ForeignKey(Habitacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.reserva_id}"
