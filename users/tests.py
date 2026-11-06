from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.conf import settings
from rest_framework.test import APIClient


class UserApiTests(TestCase):
    def setUp(self):
        self.admin = get_user_model().objects.create_superuser(
            email='admin@example.com', password='AdminClave123!', telefono='5551001000'
        )
        self.user = get_user_model().objects.create_user(
            email='cliente@example.com', password='ClienteClave123!', telefono='5552002000'
        )
        self.client = APIClient()
        response = self.client.post('/api/v1/auth/token/', {
            'email': self.admin.email, 'password': 'AdminClave123!'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

    def test_password_never_appears_and_extra_field_is_present(self):
        for path in ('/api/v1/auth/me/', '/api/v1/users/', f'/api/v1/users/{self.user.pk}/'):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertNotIn('password', str(response.data))
        self.assertEqual(self.client.get('/api/v1/auth/me/').data['telefono'], '5551001000')

    def test_edit_without_password_preserves_target_password(self):
        old_hash = self.user.password
        response = self.client.patch(f'/api/v1/users/{self.user.pk}/', {
            'telefono': '5553333333'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, old_hash)
        self.assertTrue(self.user.check_password('ClienteClave123!'))
        self.assertFalse(self.user.check_password('AdminClave123!'))

    def test_password_changes_only_when_supplied(self):
        response = self.client.patch(f'/api/v1/users/{self.user.pk}/', {
            'password': 'NuevaClave123!'
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertNotIn('password', response.data)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NuevaClave123!'))

    def test_put_without_password_also_preserves_target_password(self):
        old_hash = self.user.password
        response = self.client.put(f'/api/v1/users/{self.user.pk}/', {
            'email': self.user.email, 'username': self.user.username,
            'telefono': '5554445555',
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.password, old_hash)
        self.assertTrue(self.user.check_password('ClienteClave123!'))

    def test_create_user_response_hides_password(self):
        response = self.client.post('/api/v1/users/', {
            'email': 'nuevo@example.com', 'username': 'nuevo',
            'telefono': '5555555555', 'password': 'NuevoUsuario123!'
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertNotIn('password', response.data)
        self.assertTrue(get_user_model().objects.get(email='nuevo@example.com').check_password('NuevoUsuario123!'))

    def test_user_crud_restricted_to_admin(self):
        anonymous = APIClient()
        self.assertEqual(anonymous.get('/api/v1/users/').status_code, 401)
        response = anonymous.post('/api/v1/auth/token/', {
            'email': self.user.email, 'password': 'ClienteClave123!'
        }, format='json')
        anonymous.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(anonymous.get('/api/v1/users/').status_code, 403)
        self.assertEqual(anonymous.get('/api/v1/auth/me/').status_code, 200)

    def test_swagger_and_token_lifetime(self):
        response = self.client.get('/swagger/schema/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'APPDEWEBINTEGRALCONNOMBRECAMBIADO', response.content)
        self.assertIn(b'telefono', response.content)
        self.assertEqual(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'], timedelta(minutes=30))
