from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Entrenamiento, Ejercicio

"""
    Formulario para crear o editar un objeto Entrenamiento.
    Utiliza el modelo 'Entrenamiento' y permite capturar todos los campos definidos en él.
"""
class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento  # Especifica que este formulario está basado en el modelo Entrenamiento.
        fields = "__all__"  # Incluye todos los campos del modelo Entrenamiento en el formulario.

"""
    Formulario para crear o editar un objeto Ejercicio.
    Utiliza el modelo 'Ejercicio' y permite capturar todos los campos definidos en él.
"""
class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio  # Especifica que este formulario está basado en el modelo Ejercicio.
        fields = "__all__"  # Incluye todos los campos del modelo Ejercicio en el formulario.

"""
    Formulario para registrar un nuevo usuario en el sistema.
    Hereda de 'UserCreationForm' para incluir los campos básicos de usuario.
    Se agregan validaciones personalizadas para correo electrónico, nombre y apellidos.
"""
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    nombre = forms.CharField(max_length=25, label="Nombre", min_length=2)
    apellidos = forms.CharField(max_length=25, label="Apellidos", min_length=2)
   
    class Meta:
        model = User  # Especifica que este formulario está basado en el modelo User.
        fields = ("username", "nombre", "apellidos", "email", "password1", "password2")  # Campos que se incluirán en el formulario.
        
    """
        Valida que el correo electrónico no esté ya registrado en el sistema.
        Si el correo ya existe, se lanza una excepción de validación.
    """
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return email
    
    """
        Valida que el nombre solo contenga letras.
        Si el nombre contiene caracteres no alfabéticos, lanza una excepción de validación.
    """
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre

    """
        Valida que los apellidos solo contengan letras.
        Si los apellidos contienen caracteres no alfabéticos, lanza una excepción de validación.
    """
    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.isalpha():
            raise forms.ValidationError("Los apellidos solo deben contener letras.")
        return apellidos

    """
        Verifica que las contraseñas coincidan. Si no lo hacen, lanza una excepción de validación.
    """
    def clean_password2(self):    
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    """
        Verifica que el nombre de usuario no esté ya en uso. Si ya existe, lanza una excepción de validación.
    """
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username