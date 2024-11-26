from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Entrenamiento, Ejercicio
from .forms import EntrenamientoForm, EjercicioForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User 
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import UserRegistrationForm

def inicio(request):
    return render(request, 'paginas/inicio.html', {'show_navbar': True})

def entrenamientos(request):
    busqueda = request.GET.get('q', '') 
    entrenamientos = Entrenamiento.objects.filter(titulo__icontains=busqueda) if busqueda else Entrenamiento.objects.all()
    paginator = Paginator(entrenamientos, 3)
    num_pag = request.GET.get('page')
    obj = paginator.get_page(num_pag)

    return render(request, 'entrenamientos/index.html', {
        'entrenamientos': obj,
        'mostrar_ejercicios': False,
        'show_navbar': True,
        'busqueda': busqueda
    })

def ejercicios(request):
    busqueda = request.GET.get('q', '') 
    ejercicios = Ejercicio.objects.filter(nombre__icontains=busqueda) if busqueda else Ejercicio.objects.all()
    paginator = Paginator(ejercicios, 3)
    num_pag = request.GET.get('page')
    obj = paginator.get_page(num_pag)

    return render(request, 'entrenamientos/index.html', {
        'ejercicios': obj,
        'mostrar_ejercicios': True,
        'show_navbar': True,
        'busqueda': busqueda
    })


def detalles_entrenamiento(request, id):
    entrenamiento = get_object_or_404(Entrenamiento, id=id)
    ejercicios = entrenamiento.ejercicios.all()
    paginator = Paginator(ejercicios, 4) 
    num_pag = request.GET.get('page')  
    pagina_ejercicios = paginator.get_page(num_pag) 
    mostrar = request.GET.get('mostrar', 'descripcion') 

    return render(request, 'entrenamientos/entrenamiento.html', {
        'entrenamiento': entrenamiento,
        'ejercicios': pagina_ejercicios,
        'mostrar': mostrar,
        'show_navbar': True
    })

@login_required
def crear_entrenamiento(request):
    ejercicios = Ejercicio.objects.all()  
    formulario = EntrenamientoForm(request.POST or None, request.FILES or None)
    
    if formulario.is_valid():
        formulario.save()
        return redirect('entrenamientos')  
    
    return render(request, 'entrenamientos/crear_entrenamiento.html', {
        'formulario': formulario,
        'ejercicios': ejercicios,
        'show_navbar': True
    })
    
@login_required
def editar_entrenamiento(request, id):
    ejercicios = Ejercicio.objects.all()  
    entrenamiento = Entrenamiento.objects.get(id=id)
    formulario = EntrenamientoForm(request.POST or None, request.FILES or None, instance=entrenamiento)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('entrenamientos')
    return render(request, 'entrenamientos/editar_entrenamiento.html', {'formulario': formulario, 'ejercicios': ejercicios, 'show_navbar': True})

@login_required
def eliminar_entrenamiento(request, id):
    entrenamiento = Entrenamiento.objects.get(id=id)
    entrenamiento.delete()
    return redirect('entrenamientos')

@login_required
def crear_ejercicio(request):
    formulario = EjercicioForm(request.POST or None, request.FILES or None)
    if formulario.is_valid():
        formulario.save()
        return redirect('ejercicios')
    return render(request, 'ejercicios/crear_ejercicio.html', {'formulario': formulario, 'show_navbar': True})

@login_required
def editar_ejercicio(request, id):
    ejercicio = Ejercicio.objects.get(id=id)
    formulario = EjercicioForm(request.POST or None, request.FILES or None, instance=ejercicio)
    if formulario.is_valid() and request.POST:
        formulario.save()
        return redirect('ejercicios')
    return render(request, 'ejercicios/editar_ejercicio.html', {'formulario': formulario, 'show_navbar': True})

@login_required
def eliminar_ejercicio(request, id):
    ejercicio = Ejercicio.objects.get(id=id)
    ejercicio.delete()
    return redirect('ejercicios')

def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                usuario = form.save()
                login(request, usuario)
                return redirect('entrenamientos')
            except IntegrityError:
                form.add_error(None, "El usuario ya existe")
        else:
            return render(request, 'paginas/registro.html', {'form': form, 'show_navbar': False})
    else:
        form = UserRegistrationForm()
    return render(request, 'paginas/registro.html', {'form': form, 'show_navbar': False})


@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('inicio')


class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-5000 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-5000 text-sm focus:outline-none focus:border-gray-400 focus:bg-white mt-5'
    }))
    
def inicio_sesion(request):
    error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password) 
            if user is not None:
                login(request, user)
                return redirect('inicio')
            else:
                error = "Credenciales incorrectas, por favor inténtelo de nuevo"
    else:
        form = LoginForm()

    return render(request, 'paginas/inicio_sesion.html', {'form': form, 'error': error, 'show_navbar': False})

@login_required
def apuntarse_entrenamiento(request, id):
    entrenamiento = get_object_or_404(Entrenamiento, id=id)
    if entrenamiento in request.user.entrenamientos_apuntados.all():
        return redirect('entrenamientos')  
    request.user.entrenamientos_apuntados.add(entrenamiento)
    return redirect('entrenamientos')

@login_required
def entrenamientos_apuntados(request):
    entrenamientos = request.user.entrenamientos_apuntados.all()
    return render(request, 'entrenamientos/apuntados.html', {'entrenamientos': entrenamientos, 'show_navbar': True})

@login_required
def desapuntarse_entrenamiento(request, id):
    entrenamiento = get_object_or_404(Entrenamiento, id=id)
    request.user.entrenamientos_apuntados.remove(entrenamiento)
    return redirect(request.META.get('HTTP_REFERER', 'entrenamientos_apuntados'))
