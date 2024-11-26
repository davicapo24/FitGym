from django.contrib.auth.models import User
from django.db import models

"""
    Modelo para representar un ejercicio.
    Cada ejercicio tiene un nombre, una descripción, una imagen y una fecha de creación.
"""
class Ejercicio(models.Model):
    id = models.AutoField(primary_key=True)  # ID único y autoincremental para cada ejercicio.
    nombre = models.CharField(max_length=100, null=False, blank=False, default="", verbose_name='Nombre')  # Nombre obligatorio del ejercicio con máxima longitud de 100 caracteres.
    descripcion = models.TextField(null=False, blank=False, default="", verbose_name='Descripción')  # Descripción obligatoria del ejercicio.
    imagen = models.ImageField(
        upload_to='imagenes_ejercicio/',  # Carpeta donde se almacenarán las imágenes de los ejercicios.
        null=False, 
        blank=False, 
        default='static/private-files/ImagenDefault.webp',  # Imagen por defecto si no se proporciona una imagen.
        verbose_name='Imagen'
    )
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Fecha y hora de creación del ejercicio.

    """
        Representación en cadena del ejercicio.
        Muestra el nombre del ejercicio cuando se imprime un objeto de este modelo.
    """
    def __str__(self):
        return f"Nombre: {self.nombre}"

    """
        Sobrescribe el método delete para eliminar la imagen del ejercicio de la memoria al eliminar el objeto.
        Llama al método de eliminación de la clase base para eliminar el objeto.
    """
    def delete(self, using=None, keep_parents=False):    
        self.imagen.storage.delete(self.imagen.name)  # Elimina la imagen del almacenamiento.
        super().delete()  # Elimina el objeto Ejercicio de la base de datos.

"""
    Modelo para representar un entrenamiento.
    Cada entrenamiento tiene un título, una descripción, una lista de ejercicios asociados, 
    una imagen y una fecha de creación.
"""
class Entrenamiento(models.Model):
    id = models.AutoField(primary_key=True)  # ID único y autoincremental para cada entrenamiento.
    titulo = models.CharField(max_length=100, null=False, blank=False, default="", verbose_name='Titulo')  # Título obligatorio del entrenamiento con máxima longitud de 100 caracteres.
    descripcion = models.TextField(null=False, blank=False, default="", verbose_name='Descripción')  # Descripción obligatoria del entrenamiento.
    ejercicios = models.ManyToManyField(Ejercicio, verbose_name='Ejercicios', related_name='entrenamientos')  # Relación N:M con el modelo Ejercicio.
    imagen = models.ImageField(
        upload_to='imagenes_entrenamiento/',  # Carpeta donde se almacenarán las imágenes de los entrenamientos.
        null=False, 
        blank=False, 
        default='static/private-files/ImagenDefault.webp',  # Imagen por defecto si no se proporciona una imagen.
        verbose_name='Imagen'
    )
    creado = models.DateTimeField(auto_now_add=True, null=True, blank=True)  # Fecha y hora de creación del entrenamiento.

    """
        Representación en cadena del entrenamiento.
        Muestra el título del entrenamiento cuando se imprime un objeto de este modelo.
    """
    def __str__(self):
        return f"Titulo: {self.titulo}"

    """
        Sobrescribe el método delete para eliminar la imagen del entrenamiento de la memoria al eliminar el objeto.
        Llama al método de eliminación de la clase base para eliminar el objeto.
    """
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)  # Elimina la imagen del almacenamiento.
        super().delete()  # Elimina el objeto Entrenamiento de la base de datos.

# Se agrega un campo ManyToMany al modelo User para representar los entrenamientos apuntados por un usuario.
User.add_to_class('entrenamientos_apuntados', models.ManyToManyField(Entrenamiento, related_name='apuntados', blank=True))