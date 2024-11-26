from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Entrenamiento, Ejercicio
from .forms import UserRegistrationForm, EntrenamientoForm, EjercicioForm
from django.core.files.uploadedfile import SimpleUploadedFile

class ViewsTests(TestCase):

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

    def test_inicio_view(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/inicio.html')

    def test_cerrar_sesion_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.get(reverse('cerrar_sesion'))
        self.assertEqual(response.status_code, 302)  

    def test_inicio_sesion_view_get(self):
        response = self.client.get(reverse('inicio_sesion'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/inicio_sesion.html')

    def test_inicio_sesion_view_post(self):
        response = self.client.post(reverse('inicio_sesion'), {
            'username': 'testuser',
            'password': 'Pepeylola24!'
        })
        self.assertEqual(response.status_code, 302)  

    def test_apuntarse_entrenamiento_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('apuntarse_entrenamiento', args=[self.entrenamiento.id]))
        self.assertEqual(response.status_code, 302)  

    def test_entrenamientos_apuntados_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        self.user.entrenamientos_apuntados.add(self.entrenamiento)
        response = self.client.get(reverse('entrenamientos_apuntados'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/apuntados.html')

    def test_desapuntarse_entrenamiento_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        self.user.entrenamientos_apuntados.add(self.entrenamiento)
        response = self.client.post(reverse('desapuntarse_entrenamiento', args=[self.entrenamiento.id]))
        self.assertEqual(response.status_code, 302)  

class EntrenamientoTests(TestCase):

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

    def test_entrenamientos_view(self):
        response = self.client.get(reverse('entrenamientos'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/index.html')

    def test_ejercicios_view(self):
        response = self.client.get(reverse('ejercicios'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/index.html')

    def test_detalles_entrenamiento_view(self):
        response = self.client.get(reverse('detalles_entrenamiento', args=[self.entrenamiento.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/entrenamiento.html')

    def test_crear_entrenamiento_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.get(reverse('crear_entrenamiento'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/crear_entrenamiento.html')

    def test_crear_entrenamiento_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('crear_entrenamiento'), {
            'titulo': 'Nuevo Entrenamiento',
            'descripcion': 'Descripción del nuevo entrenamiento',
            'ejercicios': [self.ejercicio.id]
        })
        self.assertEqual(response.status_code, 302)  

    def test_editar_entrenamiento_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.get(reverse('editar_entrenamiento', args=[self.entrenamiento.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'entrenamientos/editar_entrenamiento.html')
        
    def test_editar_entrenamiento_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('editar_entrenamiento', args=[self.entrenamiento.id]), {
            'titulo': 'Entrenamiento Editado',
            'descripcion': 'Descripción editada',
            'ejercicios': [self.ejercicio.id]
        })
        self.assertEqual(response.status_code, 302)  

    def test_eliminar_entrenamiento_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('eliminar_entrenamiento', args=[self.entrenamiento.id]))
        self.assertEqual(response.status_code, 302)  

class EjercicioTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='Pepeylola24!')
        self.ejercicio = Ejercicio.objects.create(nombre='Ejercicio 1', descripcion='Descripción del ejercicio')

    def test_crear_ejercicio_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.get(reverse('crear_ejercicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ejercicios/crear_ejercicio.html')
        
    def test_crear_ejercicio_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('crear_ejercicio'), {
            'nombre': 'Nuevo Ejercicio',
            'descripcion': 'Descripción del nuevo ejercicio'
        })
        self.assertEqual(response.status_code, 302)  

    def test_editar_ejercicio_view_get(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.get(reverse('editar_ejercicio', args=[self.ejercicio.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'ejercicios/editar_ejercicio.html')
        
    def test_editar_ejercicio_view_post(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('editar_ejercicio', args=[self.ejercicio.id]), {
            'nombre': 'Ejercicio Editado',
            'descripcion': 'Descripción editada'
        })
        self.assertEqual(response.status_code, 302)  

    def test_eliminar_ejercicio_view(self):
        self.client.login(username='testuser', password='Pepeylola24!')
        response = self.client.post(reverse('eliminar_ejercicio', args=[self.ejercicio.id]))
        self.assertEqual(response.status_code, 302) 
        
class EntrenamientoFormTests(TestCase):

    def test_entrenamiento_form_valid(self):
        ejercicio = Ejercicio.objects.create(nombre='Ejercicio 1', descripcion='Descripción del ejercicio')
        form_data = {
            'titulo': 'Entrenamiento 1',
            'descripcion': 'Descripción del entrenamiento',
            'ejercicios': [ejercicio.id],
            'imagen': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        }
        form = EntrenamientoForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_entrenamiento_form_invalid(self):
        form_data = {
            'titulo': '',
            'descripcion': 'Descripción del entrenamiento',
            'ejercicios': [],
            'imagen': None
        }
        form = EntrenamientoForm(data=form_data)
        self.assertFalse(form.is_valid())

class EjercicioFormTests(TestCase):

    def test_ejercicio_form_valid(self):
        form_data = {
            'nombre': 'Ejercicio 1',
            'descripcion': 'Descripción del ejercicio',
            'imagen': SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        }
        form = EjercicioForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_ejercicio_form_invalid(self):
        form_data = {
            'nombre': '',
            'descripcion': 'Descripción del ejercicio',
            'imagen': None
        }
        form = EjercicioForm(data=form_data)
        self.assertFalse(form.is_valid())
        
class UserRegistrationFormTests(TestCase):

    def test_registro_view_get(self):
        response = self.client.get(reverse('registro'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/registro.html')
        
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

    def test_user_registration_form_invalid_email(self):
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='Pepeylola24!')
        form_data = {
            'username': 'testuser',
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'testuser@example.com',
            'password1': 'Pepeylola24!',
            'password2': 'Pepeylola24!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_user_registration_form_invalid_nombre(self):
        form_data = {
            'username': 'testuser',
            'nombre': 'Test123',
            'apellidos': 'User',
            'email': 'testuser@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('nombre', form.errors)

    def test_user_registration_form_invalid_apellidos(self):
        form_data = {
            'username': 'testuser',
            'nombre': 'Test',
            'apellidos': 'User123',
            'email': 'testuser@example.com',
            'password1': 'Testpassword123',
            'password2': 'Testpassword123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('apellidos', form.errors)

    def test_user_registration_form_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'testuser@example.com',
            'password1': 'Pepeylola24!',
            'password2': 'Lolaypepe24.'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_user_registration_form_username_exists(self):
        User.objects.create_user(username='testuser', email='testuser2@example.com', password='Pepeylola24!')
        form_data = {
            'username': 'testuser',
            'nombre': 'Test',
            'apellidos': 'User',
            'email': 'testuser3@example.com',
            'password1': 'Pepeylola24!',
            'password2': 'Pepeylola24!'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)