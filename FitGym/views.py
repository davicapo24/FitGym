from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Entrenamiento, Ejercicio
from .forms import EntrenamientoForm, EjercicioForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django import forms
from .forms import UserRegistrationForm

"""
    Vista de inicio que renderiza la página principal.
"""
def inicio(request):
    return render(request, 'paginas/inicio.html', {'show_navbar': True})

"""
    Vista que muestra todos los entrenamientos o los que coinciden con una búsqueda.
"""
def entrenamientos(request):
    busqueda = request.GET.get('q', '') 
    entrenamientos = Entrenamiento.objects.filter(titulo__icontains=busqueda) if busqueda else Entrenamiento.objects.all()
    paginator = Paginator(entrenamientos, 3)  # Paginación de los entrenamientos de 3 en 3
    num_pag = request.GET.get('page')  # Obtiene la página actual
    obj = paginator.get_page(num_pag)  # Obtiene los entrenamientos correspondientes a la página solicitada

    return render(request, 'entrenamientos/index.html', {
        'entrenamientos': obj,
        'mostrar_ejercicios': False, 
        'show_navbar': True,
        'busqueda': busqueda
    })

"""
    Vista que muestra todos los ejercicios o los que coinciden con una búsqueda.
"""
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

"""
    Vista que muestra los detalles de un entrenamiento específico, incluyendo sus ejercicios.
"""
def detalles_entrenamiento(request, id):
    entrenamiento = get_object_or_404(Entrenamiento, id=id)  # Obtiene el entrenamiento o muestra un error 404 si no existe
    ejercicios = entrenamiento.ejercicios.all()  # Obtiene los ejercicios asociados al entrenamiento
    paginator = Paginator(ejercicios, 4) 
    num_pag = request.GET.get('page') 
    pagina_ejercicios = paginator.get_page(num_pag)  # Obtiene los ejercicios correspondientes a la página solicitada
    mostrar = request.GET.get('mostrar', 'descripcion')  # Define qué parte mostrar del entrenamiento (descripcion o ejercicios)

    return render(request, 'entrenamientos/entrenamiento.html', {
        'entrenamiento': entrenamiento,
        'ejercicios': pagina_ejercicios,
        'mostrar': mostrar,
        'show_navbar': True
    })

"""
    Vista protegida por login para crear un nuevo entrenamiento.
"""
@login_required
def crear_entrenamiento(request):
    ejercicios = Ejercicio.objects.all()  # Obtiene todos los ejercicios disponibles
    formulario = EntrenamientoForm(request.POST or None, request.FILES or None)  # Inicializa el formulario de entrenamiento
    
    if formulario.is_valid():  # Si el formulario es válido, guarda el nuevo entrenamiento
        formulario.save()
        return redirect('entrenamientos') 
    
    return render(request, 'entrenamientos/crear_entrenamiento.html', {
        'formulario': formulario,
        'ejercicios': ejercicios,
        'show_navbar': True
    })

"""
    Vista protegida por login para editar un entrenamiento existente.
"""
@login_required
def editar_entrenamiento(request, id):
    ejercicios = Ejercicio.objects.all()  # Obtiene todos los ejercicios disponibles
    entrenamiento = Entrenamiento.objects.get(id=id)  # Obtiene el entrenamiento a editar
    formulario = EntrenamientoForm(request.POST or None, request.FILES or None, instance=entrenamiento)  # Rellena el formulario con los datos del entrenamiento
    
    if formulario.is_valid() and request.POST:  # Si el formulario es válido y se envía, guarda los cambios
        formulario.save()
        return redirect('entrenamientos') 
    
    return render(request, 'entrenamientos/editar_entrenamiento.html', {'formulario': formulario, 'ejercicios': ejercicios, 'show_navbar': True})

"""
    Vista protegida por login para eliminar un entrenamiento.
"""
@login_required
def eliminar_entrenamiento(request, id):
    entrenamiento = Entrenamiento.objects.get(id=id)  # Obtiene el entrenamiento a eliminar
    entrenamiento.delete() 
    return redirect('entrenamientos')

"""
    Vista protegida por login para crear un nuevo ejercicio.
"""
@login_required
def crear_ejercicio(request):
    formulario = EjercicioForm(request.POST or None, request.FILES or None)  # Inicializa el formulario de ejercicio
    if formulario.is_valid():  # Si el formulario es válido, guarda el nuevo ejercicio
        formulario.save()
        return redirect('ejercicios') 
    return render(request, 'ejercicios/crear_ejercicio.html', {'formulario': formulario, 'show_navbar': True})

"""
    Vista protegida por login para editar un ejercicio existente.
"""
@login_required
def editar_ejercicio(request, id):
    ejercicio = Ejercicio.objects.get(id=id)  # Obtiene el ejercicio a editar
    formulario = EjercicioForm(request.POST or None, request.FILES or None, instance=ejercicio)  # Rellena el formulario con los datos del ejercicio
    
    if formulario.is_valid() and request.POST:  # Si el formulario es válido y se envía, guarda los cambios
        formulario.save()
        return redirect('ejercicios')  
    
    return render(request, 'ejercicios/editar_ejercicio.html', {'formulario': formulario, 'show_navbar': True})

"""
    Vista protegida por login para eliminar un ejercicio.
"""
@login_required
def eliminar_ejercicio(request, id):
    ejercicio = Ejercicio.objects.get(id=id)  # Obtiene el ejercicio a eliminar
    ejercicio.delete() 
    return redirect('ejercicios') 

"""
    Vista para registrar un nuevo usuario.
"""
def registro(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)  # Inicializa el formulario de registro
        if form.is_valid():  # Si el formulario es válido, guarda el usuario y lo loguea
            try:
                usuario = form.save()
                login(request, usuario)
                return redirect('entrenamientos')  
            except IntegrityError:  # Si hay un error de integridad (por ejemplo, el usuario ya existe), muestra un mensaje de error
                form.add_error(None, "El usuario ya existe")
        else:
            return render(request, 'paginas/registro.html', {'form': form, 'show_navbar': False})
    else:
        form = UserRegistrationForm()  # Si la solicitud no es POST, muestra un formulario vacío
    return render(request, 'paginas/registro.html', {'form': form, 'show_navbar': False})

"""
    Vista para cerrar sesión.
"""
@login_required
def cerrar_sesion(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('inicio')

"""
    Formulario de inicio de sesión con campos personalizados para username y password.
"""
class LoginForm(forms.Form):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-5000 text-sm focus:outline-none focus:border-gray-400 focus:bg-white'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'w-full px-8 py-4 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-5000 text-sm focus:outline-none focus:border-gray-400 focus:bg-white mt-5'
    }))

"""
    Vista para el inicio de sesión de un usuario.
"""
def inicio_sesion(request):
    error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') 
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)  # Autentica al usuario
            if user is not None:
                login(request, user)  # Inicia sesión si las credenciales son correctas
                return redirect('inicio')
            else:
                error = "Credenciales incorrectas, por favor inténtelo de nuevo"  # Si las credenciales son incorrectas, muestra un mensaje de error
    else:
        form = LoginForm()  # Si la solicitud no es POST, muestra un formulario vacío

    return render(request, 'paginas/inicio_sesion.html', {'form': form, 'error': error, 'show_navbar': False})

"""
    Vista protegida por login para apuntarse a un entrenamiento.
"""
@login_required
def apuntarse_entrenamiento(request, id):
    entrenamiento = get_object_or_404(Entrenamiento, id=id) 
    if entrenamiento in request.user.entrenamientos_apuntados.all():
        return redirect('entrenamientos')  # Si el usuario ya está apuntado, redirige a la vista de entrenamientos
    request.user.entrenamientos_apuntados.add(entrenamiento)  # Si no está apuntado, lo agrega a la lista de entrenamientos del usuario
    return redirect('entrenamientos')

"""
    Vista protegida por login que muestra los entrenamientos a los que el usuario está apuntado.
"""
@login_required
def entrenamientos_apuntados(request):
    entrenamientos = request.user.entrenamientos_apuntados.all()  # Obtiene los entrenamientos apuntados por el usuario
    return render(request, 'entrenamientos/apuntados.html', {'entrenamientos': entrenamientos, 'show_navbar': True})

"""
    Vista protegida por login para desapuntarse de un entrenamiento.
"""
@login_required
def desapuntarse_entrenamiento(request, id):
    entrenamiento = get_object_or_404(Entrenamiento, id=id) 
    request.user.entrenamientos_apuntados.remove(entrenamiento)  # Elimina el entrenamiento de la lista de entrenamientos apuntados del usuario
    return redirect(request.META.get('HTTP_REFERER', 'entrenamientos_apuntados'))  # Redirige a la página anterior