# Create your views here.
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Administrador


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
    return render(request,"inicio.html")



#EXAMPLES
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
