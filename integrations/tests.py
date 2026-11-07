from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from users.models import User


class IntegrationEndpointTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='viewer@example.com', password='StrongPass123!')
        self.client = APIClient()

    def test_external_endpoints_require_jwt(self):
        for path in ('/api/v1/external/avatar-scenes/', '/api/v1/external/soap/capital/'):
            self.assertEqual(self.client.get(path).status_code, 401)

    def test_soap_response_is_returned_from_service(self):
        self.client.force_authenticate(self.user)
        with patch('integrations.views.country_capital', return_value='Mexico City'):
            result = self.client.get('/api/v1/external/soap/capital/?pais=MX')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data['capital'], 'Mexico City')
        self.assertEqual(result.data['pais'], 'MX')

    def test_avatar_images_are_returned_from_service(self):
        self.client.force_authenticate(self.user)
        images = [{'serie': 'The Legend of Korra', 'imagen': 'https://example.com/korra.jpg'}]
        with patch('integrations.views.avatar_character_images', return_value=images):
            result = self.client.get('/api/v1/external/avatar-scenes/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.data['fuente'], 'Last Airbender API')
        self.assertEqual(result.data['imagenes'], images)
