"""
URL configuration for software_hotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hotel.views import (inicio, busqueda, resultados,
                        catalogo, detalle, metodo_pago,
                        realizado, inicio_sesion_adm, registrarse_adm,
                        registrarse_adm_done, inicio_sesion_adm_done, cerrar_sesion_adm,
                        menu_adm, reporte, reporte_done,
                        modificar_habitacion_adm, modificar_habitacion_adm_done, listar_reportes,
                        ver_reporte, lista_reserva, editar_reserva,
                        editar_reserva_done, eliminar_reserva_done, listar_reserva_equipos,
                        ver_reserva_equipo, registro_cli, registro_cli_done,
                        iniciar_sesion_cli, iniciar_sesion_cli_done, cerrar_sesion_cli,
                        datos_cliente, datos_cliente_done,
                        editar_usuario, listar_usuarios,
                        editar_usuario_done)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', inicio, name="inicio"),
    path('busqueda/', busqueda, name="busqueda"),
    path('resultados/', resultados, name="resultados"),
    path('catalogo/', catalogo, name="catalogo"),
    path('detalle/', detalle, name="detalle"),
    path('metodo_pago/', metodo_pago, name="metodo_pago"),
    path('realizado/', realizado, name="realizado"),
    path('inicio_sesion_adm/', inicio_sesion_adm, name="inicio_sesion_adm"),
    path('inicio_sesion_adm_done/', inicio_sesion_adm_done,name="inicio_sesion_adm_done"),
    path('registrarse_adm/', registrarse_adm, name="registrarse_adm"),
    path('registrarse_adm_done/', registrarse_adm_done,name="registrarse_adm_done"),
    path('menu_adm/', menu_adm, name="menu_adm"),
    path('reporte/', reporte, name="reporte"),
    path('reporte_done/', reporte_done, name="reporte_done"),
    path('modificar_habitacion_adm/', modificar_habitacion_adm,name="modificar_habitacion_adm"),
    path('modificar_habitacion_adm_done/', modificar_habitacion_adm_done,name="modificar_habitacion_adm_done"),
    path('cerrar_sesion_adm/', cerrar_sesion_adm, name="cerrar_sesion_adm"),
    path('listar_reportes/', listar_reportes, name="listar_reportes"),
    path('ver_reporte/', ver_reporte, name="ver_reporte"),
    path('lista_reserva/', lista_reserva, name="lista_reserva"),
    path('editar_reserva/', editar_reserva, name="editar_reserva"),
    path('editar_reserva_done/', editar_reserva_done, name="editar_reserva_done"),
    path('eliminar_reserva_done/', eliminar_reserva_done,name="eliminar_reserva_done"),
    path('listar_reserva_equipos/', listar_reserva_equipos,name="listar_reserva_equipos"),
    path('ver_reserva_equipo/', ver_reserva_equipo, name="ver_reserva_equipo"),
    path('registro_cli/', registro_cli, name="registro_cli"),
    path('registro_cli_done/', registro_cli_done, name="registro_cli_done"),
    path('iniciar_sesion_cli/', iniciar_sesion_cli, name="iniciar_sesion_cli"),
    path('iniciar_sesion_cli_done/', iniciar_sesion_cli_done, name="iniciar_sesion_cli_done"),
    path('cerrar_sesion_cli/', cerrar_sesion_cli, name="cerrar_sesion_cli"),
    path('datos_cliente/', datos_cliente, name="datos_cliente"),
    path('datos_cliente_done/', datos_cliente_done, name="datos_cliente_done"),
    path('listar_usuarios/', listar_usuarios, name="listar_usuarios"),
    path('editar_usuario/', editar_usuario, name="editar_usuario"),
    path('editar_usuario_done/', editar_usuario_done, name="editar_usuario_done"),

]
