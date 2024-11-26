from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Entrenamiento, Ejercicio
from .forms import UserRegistrationForm, EntrenamientoForm, EjercicioForm
from django.core.files.uploadedfile import SimpleUploadedFile

"""
    Clase de prueba para las vistas del proyecto.
    Contiene pruebas para las vistas relacionadas con apuntarse a entrenamientos, 
    inicio de sesión y registro de usuario.
"""
class ViewsTests(TestCase):

    """
        Configura el entorno de prueba.
        Crea un usuario, un ejercicio y un entrenamiento para ser utilizados en las pruebas.
    """
    def setUp(self):
        self.client = Client()  # Inicializa el cliente para realizar peticiones HTTP.
        self.user = User.objects.create_user(username='testuser', password='Pepeylola24!')  # Crea un usuario de prueba.
        self.ejercicio = Ejercicio.objects.create(
            nombre='Ejercicio 1',
            descripcion='Descripción del ejercicio',
            imagen=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  # Crea un ejercicio de prueba.
        )
        self.entrenamiento = Entrenamiento.objects.create(
            titulo='Entrenamiento 1',
            descripcion='Descripción del entrenamiento',
            imagen=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  # Crea un entrenamiento de prueba.
        )
        self.entrenamiento.ejercicios.add(self.ejercicio)  # Asocia el ejercicio al entrenamiento.

    """
        Prueba para verificar si la vista de inicio carga correctamente.
    """
    def test_inicio_view(self):        
        response = self.client.get(reverse('inicio'))  # Realiza una petición GET a la vista 'inicio'.
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'paginas/inicio.html')  

    """
        Prueba para verificar si la vista de cerrar sesión funciona correctamente.
    """
    def test_cerrar_sesion_view(self):        
        self.client.login(username='testuser', password='Pepeylola24!')  # Realiza login del usuario de prueba.
        response = self.client.get(reverse('cerrar_sesion'))  
        self.assertEqual(response.status_code, 302)  

    """
        Prueba para verificar si la vista de inicio de sesión se carga correctamente en GET.
    """
    def test_inicio_sesion_view_get(self):        
        response = self.client.get(reverse('inicio_sesion')) 
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'paginas/inicio_sesion.html')  
        
    """
        Prueba para verificar si la vista de inicio de sesión funciona correctamente en POST.
    """
    def test_inicio_sesion_view_post(self):
        response = self.client.post(reverse('inicio_sesion'), {
            'username': 'testuser',
            'password': 'Pepeylola24!'  # Realiza un POST con las credenciales del usuario de prueba.
        })
        self.assertEqual(response.status_code, 302)

    """
        Prueba para verificar si un usuario puede apuntarse a un entrenamiento correctamente.
    """
    def test_apuntarse_entrenamiento_view(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.post(reverse('apuntarse_entrenamiento', args=[self.entrenamiento.id]))  # Realiza una petición POST para apuntarse al entrenamiento.
        self.assertEqual(response.status_code, 302)  

    """
        Prueba para verificar si la vista de entrenamientos apuntados carga correctamente.
    """
    def test_entrenamientos_apuntados_view(self):        
        self.client.login(username='testuser', password='Pepeylola24!')  
        self.user.entrenamientos_apuntados.add(self.entrenamiento)  # Asocia el entrenamiento al usuario.
        response = self.client.get(reverse('entrenamientos_apuntados')) 
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/apuntados.html')  

    """
        Prueba para verificar si un usuario puede desapuntarse de un entrenamiento correctamente.
    """
    def test_desapuntarse_entrenamiento_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')  
        self.user.entrenamientos_apuntados.add(self.entrenamiento) 
        response = self.client.post(reverse('desapuntarse_entrenamiento', args=[self.entrenamiento.id]))  # Realiza una petición POST para desapuntarse del entrenamiento.
        self.assertEqual(response.status_code, 302)  

"""
    Clase de prueba para las vistas relacionadas con el modelo de entrenamiento.
"""
class EntrenamientoTests(TestCase):

    """
        Configura el entorno de prueba para los entrenamientos.
        Crea un usuario, un ejercicio y un entrenamiento para ser utilizados en las pruebas.
    """
    def setUp(self):
        self.client = Client() 
        self.user = User.objects.create_user(username='testuser', password='Pepeylola24!') 
        self.ejercicio = Ejercicio.objects.create(
            nombre='Ejercicio 1',
            descripcion='Descripción del ejercicio',
            imagen=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  
        )
        self.entrenamiento = Entrenamiento.objects.create(
            titulo='Entrenamiento 1',
            descripcion='Descripción del entrenamiento',
            imagen=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  
        )
        self.entrenamiento.ejercicios.add(self.ejercicio)  
        
    """
        Prueba para verificar si la vista de entrenamientos carga correctamente.
    """
    def test_entrenamientos_view(self):
        response = self.client.get(reverse('entrenamientos'))  
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'entrenamientos/index.html') 

    """
        Prueba para verificar si la vista de ejercicios carga correctamente.
    """
    def test_ejercicios_view(self):
        response = self.client.get(reverse('ejercicios')) 
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'entrenamientos/index.html')  

    """
        Prueba para verificar si la vista de detalles de un entrenamiento carga correctamente.
    """
    def test_detalles_entrenamiento_view(self):
        response = self.client.get(reverse('detalles_entrenamiento', args=[self.entrenamiento.id])) 
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'entrenamientos/entrenamiento.html') 

    """
         Prueba para verificar si la vista para crear un entrenamiento se carga correctamente en GET.
    """
    def test_crear_entrenamiento_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.get(reverse('crear_entrenamiento'))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'entrenamientos/crear_entrenamiento.html') 

    """
        Prueba para verificar si la vista para crear un entrenamiento funciona correctamente en POST.
    """
    def test_crear_entrenamiento_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.post(reverse('crear_entrenamiento'), {
            'titulo': 'Nuevo Entrenamiento',
            'descripcion': 'Descripción del nuevo entrenamiento',
            'ejercicios': [self.ejercicio.id]  
        })
        self.assertEqual(response.status_code, 302)  

"""
    Clase de prueba para las vistas relacionadas con el modelo de ejercicio.
"""
class EjercicioTests(TestCase):

    """
        Configura el entorno de prueba para los ejercicios.
    """
    def setUp(self):
        self.client = Client() 
        self.user = User.objects.create_user(username='testuser', password='Pepeylola24!')  
        self.ejercicio = Ejercicio.objects.create(
            nombre='Ejercicio de Prueba',
            descripcion='Descripción del ejercicio de prueba',
            imagen=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  
        )

    """
        Prueba para verificar si la vista para crear un ejercicio se carga correctamente.
    """
    def test_crear_ejercicio_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.get(reverse('crear_ejercicio'))  
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ejercicios/crear_ejercicio.html')

    """
        Prueba para verificar si la vista para crear un ejercicio funciona correctamente en POST.
    """
    def test_crear_ejercicio_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.post(reverse('crear_ejercicio'), {
            'nombre': 'Nuevo Ejercicio',
            'descripcion': 'Descripción del nuevo ejercicio'
        })
        self.assertEqual(response.status_code, 302)

    """
        Prueba para verificar si la vista de edición de un ejercicio se carga correctamente en GET.
        El usuario debe estar autenticado y debe acceder a la vista para editar un ejercicio existente.
    """
    def test_editar_ejercicio_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.get(reverse('editar_ejercicio', args=[self.ejercicio.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ejercicios/editar_ejercicio.html')

    """
        Prueba para verificar si la vista de edición de un ejercicio se procesa correctamente en POST.
        El usuario debe ser capaz de editar la información del ejercicio.
    """
    def test_editar_ejercicio_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!')  
        response = self.client.post(reverse('editar_ejercicio', args=[self.ejercicio.id]), {
            'nombre': 'Ejercicio Editado',  
            'descripcion': 'Descripción editada'  
        })
        self.assertEqual(response.status_code, 302)

    """
        Prueba para verificar si la vista de eliminación de un ejercicio funciona correctamente.
        El usuario debe ser capaz de eliminar un ejercicio existente.
    """
    def test_eliminar_ejercicio_view(self):
        self.client.login(username='testuser', password='Pepeylola24!') 
        response = self.client.post(reverse('eliminar_ejercicio', args=[self.ejercicio.id])) 
        self.assertEqual(response.status_code, 302)

"""
    Clase de prueba para el formulario de entrenamiento.
"""
class EntrenamientoFormTests(TestCase):

    """
        Prueba para verificar que el formulario de creación de un entrenamiento sea válido con datos correctos.
        Se crea un ejercicio y se asocia al formulario.
    """
    def test_entrenamiento_form_valid(self):
        ejercicio = Ejercicio.objects.create(nombre='Ejercicio 1', descripcion='Descripción del ejercicio')  
        form_data = {
            'titulo': 'Entrenamiento 1',  
            'descripcion': 'Descripción del entrenamiento',  
            'ejercicios': [ejercicio.id],  
            'imagen': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')  
        }
        form = EntrenamientoForm(data=form_data) # Crea una instancia del formulario con los datos.
        self.assertTrue(form.is_valid()) # Verifica que el formulario sea válido.

    """
        Prueba para verificar que el formulario de creación de un entrenamiento sea inválido con datos incorrectos.
        Faltan datos esenciales como el título y los ejercicios.
    """
    def test_entrenamiento_form_invalid(self):
        form_data = {
            'titulo': '',
            'descripcion': 'Descripción del entrenamiento',  
            'ejercicios': [],  
            'imagen': None  
        }
        form = EntrenamientoForm(data=form_data)  # Crea una instancia del formulario con los datos.
        self.assertFalse(form.is_valid())  # Verifica que el formulario sea inválido.

"""
    Clase de prueba para el formulario de ejercicio.
"""
class EjercicioFormTests(TestCase):

    """
        Prueba para verificar que el formulario de creación de un ejercicio sea válido con datos correctos.
        Se proporciona un nombre, descripción e imagen.
    """
    def test_ejercicio_form_valid(self):
        form_data = {
            'nombre': 'Ejercicio 1', 
            'descripcion': 'Descripción del ejercicio',  
            'imagen': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        }
        form = EjercicioForm(data=form_data) 
        self.assertTrue(form.is_valid())

    """
        Prueba para verificar que el formulario de creación de un ejercicio sea inválido con datos incorrectos.
        El nombre y la imagen están vacíos.
    """
    def test_ejercicio_form_invalid(self):
        form_data = {
            'nombre': '',  
            'descripcion': 'Descripción del ejercicio',  
            'imagen': None 
        }
        form = EjercicioForm(data=form_data)  
        self.assertFalse(form.is_valid()) 

"""
    Clase de prueba para el formulario de registro de usuario.
"""
class UserRegistrationFormTests(TestCase):

    """
        Prueba para verificar si la vista de registro de usuario se carga correctamente en GET.
    """
    def test_registro_view_get(self):
        response = self.client.get(reverse('registro'))  
        self.assertEqual(response.status_code, 200)  
        self.assertTemplateUsed(response, 'paginas/registro.html')  

    """
        Prueba para verificar si el formulario de registro de usuario es válido con datos correctos.
        El formulario se debe enviar correctamente con un usuario, nombre, apellidos, email y contraseña válidos.
    """
    def test_user_registration_form_valid(self):
        form_data = {
            'username': 'testuser', 
            'nombre': 'Test', 
            'apellidos': 'User',  
            'email': 'testuser@example.com',  
            'password1': 'Pepeylola24!', 
            'password2': 'Pepeylola24!' 
        }
        form = UserRegistrationForm(data=form_data)  
        self.assertTrue(form.is_valid()) 

    """
        Prueba para verificar que el formulario de registro de usuario sea inválido cuando el email ya está registrado.
        El formulario debe fallar y mostrar un error en el campo 'email'.
    """
    def test_user_registration_form_invalid_email(self):
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='Pepeylola24!') 
        form_data = {
            'username': 'testuser',  
            'nombre': 'Test',
            'apellidos': 'User',  
            'email': 'testuser@example.com', # Email ya existente
            'password1': 'Pepeylola24!', 
            'password2': 'Pepeylola24!' 
        }
        form = UserRegistrationForm(data=form_data) 
        self.assertFalse(form.is_valid())  
        self.assertIn('email', form.errors)  # Verifica que el error esté en el campo 'email'.

    """
        Prueba para verificar que el formulario de registro de usuario sea inválido cuando el nombre contiene caracteres no válidos.
    """
    def test_user_registration_form_invalid_nombre(self):
        form_data = {
            'username': 'testuser',  
            'nombre': 'Test123',  # Nombre inválido (contiene números).
            'apellidos': 'User',  
            'email': 'testuser@example.com',  
            'password1': 'Testpassword123',  
            'password2': 'Testpassword123' 
        }
        form = UserRegistrationForm(data=form_data)  
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)  # Verifica que el error esté en el campo 'nombre'.

    """
        Prueba para verificar que el formulario de registro de usuario sea inválido cuando los apellidos contienen caracteres no válidos.
    """
    def test_user_registration_form_invalid_apellidos(self):
        form_data = {
            'username': 'testuser',  
            'nombre': 'Test',  
            'apellidos': 'User123',  # Apellidos inválidos (contienen números).
            'email': 'testuser@example.com',  
            'password1': 'Testpassword123', 
            'password2': 'Testpassword123'  
        }
        form = UserRegistrationForm(data=form_data) 
        self.assertFalse(form.is_valid())  
        self.assertIn('apellidos', form.errors)  # Verifica que el error esté en el campo 'apellidos'.

    """
        Prueba para verificar que el formulario de registro de usuario sea inválido cuando las contraseñas no coinciden.
    """
    def test_user_registration_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',  
            'nombre': 'Test',  
            'apellidos': 'User', 
            'email': 'testuser@example.com',  
            'password1': 'Pepeylola24!',  
            'password2': 'Lolaypepe24.'  # Contraseña no coincide.
        }
        form = UserRegistrationForm(data=form_data)  
        self.assertFalse(form.is_valid())  
        self.assertIn('password2', form.errors)  # Verifica que el error esté en el campo 'password2'.

    """
       Prueba para verificar que el formulario de registro de usuario sea inválido cuando el nombre de usuario ya existe.
    """
    def test_user_registration_form_username_exists(self):
        User.objects.create_user(username='testuser', email='testuser2@example.com', password='Pepeylola24!')  
        form_data = {
            'username': 'testuser',  # Nombre de usuario duplicado.
            'nombre': 'Test', 
            'apellidos': 'User', 
            'email': 'testuser3@example.com',  
            'password1': 'Pepeylola24!',  
            'password2': 'Pepeylola24!' 
        }
        form = UserRegistrationForm(data=form_data)  
        self.assertFalse(form.is_valid())  
        self.assertIn('username', form.errors)  # Verifica que el error esté en el campo 'username'.