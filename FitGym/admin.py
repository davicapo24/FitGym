from django.contrib import admin
from .models import Entrenamiento, Ejercicio

# Register your models here.

"""
    Personaliza la interfaz de administración para el modelo Entrenamiento.
"""
class EntrenamientoAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', )  # Establece el campo 'creado' como de solo lectura

"""
    Personaliza la interfaz de administración para el modelo Ejercicio.
"""
class EjercicioAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', )  # Establece el campo 'creado' como de solo lectura

# Registra los modelos 'Entrenamiento' y 'Ejercicio' en el sitio de administración de Django
admin.site.register(Entrenamiento, EntrenamientoAdmin)
admin.site.register(Ejercicio, EjercicioAdmin)
