from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('entrenamientos', views.entrenamientos, name='entrenamientos'),
    path('ejercicios', views.ejercicios, name='ejercicios'),
    path('entrenamiento/<int:id>/', views.detalles_entrenamiento, name='detalles_entrenamiento'),
    path('entrenamientos/crear', views.crear_entrenamiento, name='crear_entrenamiento'),
    path('entrenamientos/editar', views.editar_entrenamiento, name='editar_entrenamiento'),
    path('entrenamientos/eliminar/<int:id>', views.eliminar_entrenamiento, name='eliminar_entrenamiento'),
    path('entrenamientos/editar/<int:id>', views.editar_entrenamiento, name='editar_entrenamiento'),
    path('ejercicios/crear', views.crear_ejercicio, name='crear_ejercicio'),
    path('ejercicios/editar', views.editar_ejercicio, name='editar_ejercicio'),
    path('ejercicios/eliminar/<int:id>', views.eliminar_ejercicio, name='eliminar_ejercicio'),
    path('ejercicios/editar/<int:id>', views.editar_ejercicio, name='editar_ejercicio'),
    path('registro', views.registro, name='registro'),
    path('cerrar_sesion', views.cerrar_sesion, name='cerrar_sesion'),
    path('inicio_sesion', views.inicio_sesion, name='inicio_sesion'),
    path('entrenamiento/<int:id>/apuntarse/', views.apuntarse_entrenamiento, name='apuntarse_entrenamiento'),
    path('entrenamiento/<int:id>/desapuntarse/', views.desapuntarse_entrenamiento, name='desapuntarse_entrenamiento'),
    path('entrenamientos/apuntados', views.entrenamientos_apuntados, name='entrenamientos_apuntados'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
