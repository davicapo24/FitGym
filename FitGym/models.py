from django.contrib.auth.models import User
from django.db import models

class Ejercicio(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    descripcion = models.TextField(null=True, verbose_name='Descripción')
    imagen = models.ImageField(upload_to='imagenes_ejercicio/', null=False, blank=False, default='static/private-files/ImagenDefault.webp', verbose_name='Imagen')
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Nombre: {self.nombre}"

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()


class Entrenamiento(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=100, verbose_name='Titulo')
    descripcion = models.TextField(null=True, verbose_name='Descripción')
    ejercicios = models.ManyToManyField(Ejercicio, verbose_name='Ejercicios', related_name='entrenamientos')
    imagen = models.ImageField(upload_to='imagenes_entrenamiento/', null=False, blank=False, default='static/private-files/ImagenDefault.webp', verbose_name='Imagen')
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"Titulo: {self.titulo}"

    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()

User.add_to_class('entrenamientos_apuntados', models.ManyToManyField(Entrenamiento, related_name='apuntados', blank=True))