from django.shortcuts import render, redirect
from django.contrib import messages 

# Decorator para ver si es administrador
def admin_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.groups.filter(name='administrador').exists():
            return function(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrap

#Decorator para ver si es usuario de la aplicacion del site
def videocorn_required(function):
    def wrap(request, *args, **kwargs):
        if (request.user.groups.filter(name='administrador').exists()) or (request.user.groups.filter(name='usuario_videocorn').exists()):
            return function(request, *args, **kwargs)
        else:
            #Creamos mensaje
            messages.error(request, 'Este usuario no tiene acceso a Videocorn.')
            return redirect('log_in')
    return wrap