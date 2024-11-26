from django.contrib import admin
from .models import Entrenamiento, Ejercicio

# Register your models here.

class EntrenamientoAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', )
class EjercicioAdmin(admin.ModelAdmin):
    readonly_fields = ('creado', )
    
admin.site.register(Entrenamiento, EntrenamientoAdmin)
admin.site.register(Ejercicio, EjercicioAdmin)

