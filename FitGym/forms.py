from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Entrenamiento, Ejercicio

class EntrenamientoForm(forms.ModelForm):
    class Meta:
        model = Entrenamiento
        fields = "__all__"
    
        
class EjercicioForm(forms.ModelForm):
    class Meta:
        model = Ejercicio
        fields = "__all__"
           
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    nombre = forms.CharField(max_length=25, label="Nombre", min_length=2)
    apellidos = forms.CharField(max_length=25, label="Apellidos", min_length=2)
   
    class Meta:
        model = User
        fields = ("username", "nombre", "apellidos", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("El correo electrónico ya está registrado.")
        return email
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not nombre.isalpha():
            raise forms.ValidationError("El nombre solo debe contener letras.")
        return nombre

    def clean_apellidos(self):
        apellidos = self.cleaned_data.get('apellidos')
        if not apellidos.isalpha():
            raise forms.ValidationError("Los apellidos solo deben contener letras.")
        return apellidos

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nombre de usuario ya está en uso.")
        return username