from django.apps import AppConfig

"""
    Configuración de la aplicación FitGym.
    
    La clase FitgymConfig se utiliza para definir la configuración de la aplicación Django 
    llamada 'FitGym'. Es una subclase de AppConfig que proporciona configuraciones y 
    características adicionales para la aplicación dentro del proyecto Django.
"""
class FitgymConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField" # Establece el tipo de campo predeterminado para las claves primarias de los modelos.
    name = "FitGym" # Especifica el nombre de la aplicación.