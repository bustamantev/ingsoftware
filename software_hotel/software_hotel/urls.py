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
from hotel.views import inicio, busqueda, resultados, catalogo, detalle, metodo_pago, realizado, inicio_sesion_adm, registrarse_adm, registrarse_adm_done, inicio_sesion_adm_done, cerrar_sesion_adm, menu_adm, reporte, reporte_done, modificar_habitacion_adm, modificar_habitacion_adm_done

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
    path('inicio_sesion_adm_done/', inicio_sesion_adm_done, name="inicio_sesion_adm_done"),
    path('registrarse_adm/', registrarse_adm, name="registrarse_adm"),
    path('registrarse_adm_done/', registrarse_adm_done, name="registrarse_adm_done"),
    path('menu_adm/', menu_adm, name="menu_adm"),
    path('reporte/', reporte, name="reporte"),
    path('reporte_done/', reporte_done, name="reporte_done"),
    path('modificar_habitacion_adm/', modificar_habitacion_adm, name="modificar_habitacion_adm"),
    path('modificar_habitacion_adm_done/', modificar_habitacion_adm_done, name="modificar_habitacion_adm_done"),
    path('cerrar_sesion_adm/', cerrar_sesion_adm, name="cerrar_sesion_adm"),

]
