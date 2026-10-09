from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from decimal import Decimal
from rest_framework.test import APIClient

from .models import Category, Product


class CategoryPracticeTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username='jwt_test_user', password='ClaveSegura123!'
        )
        cls.electronics = Category.objects.create(name='Electrónica')
        cls.clothing = Category.objects.create(name='Ropa')
        cls.mouse = Product.objects.create(
            name='Mouse', description='Mouse USB', price='250.00',
            category=cls.electronics,
        )
        Product.objects.create(
            name='Playera', description='Playera de algodón', price='180.00',
            category=cls.clothing,
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_categories_and_admin_registration(self):
        response = self.client.get('/api/categories/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual({c['name'] for c in response.data}, {'Electrónica', 'Ropa'})
        self.assertTrue(admin.site.is_registered(Category))
        self.assertTrue(admin.site.is_registered(Product))

    def test_product_category_is_a_name(self):
        response = self.client.get('/api/products/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['category'], 'Electrónica')
        self.assertNotIn('category_id', response.data[0])

    def test_filter_excludes_other_categories(self):
        response = self.client.get('/api/products/', {'category': self.electronics.pk})
        self.assertEqual(response.status_code, 200)
        self.assertEqual([p['id'] for p in response.data], [self.mouse.pk])

    def test_invalid_filter_returns_a_validation_error(self):
        response = self.client.get('/api/products/', {'category': 'invalid'})
        self.assertEqual(response.status_code, 400)

    def test_api_can_still_create_and_reassign_products(self):
        response = self.client.post('/api/products/', {
            'name': 'Teclado', 'description': 'Teclado USB', 'price': '450.00',
            'category_id': self.electronics.pk,
        }, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['category'], 'Electrónica')
        response = self.client.patch(f"/api/products/{response.data['id']}/", {
            'category_id': self.clothing.pk,
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['category'], 'Ropa')

    def test_product_requires_a_valid_category(self):
        data = {'name': 'Teclado', 'description': 'USB', 'price': '450.00'}
        self.assertEqual(self.client.post('/api/products/', data).status_code, 400)
        data['category_id'] = 99999
        self.assertEqual(self.client.post('/api/products/', data).status_code, 400)

    def test_previous_api_route_remains_available(self):
        self.assertEqual(self.client.get('/api/v1/products/').status_code, 200)

    def test_protected_endpoint_rejects_requests_without_token(self):
        anonymous_client = APIClient()
        response = anonymous_client.get('/api/products/')
        self.assertEqual(response.status_code, 401)

    def test_token_allows_access_to_products(self):
        anonymous_client = APIClient()
        token_response = anonymous_client.post('/api/token/', {
            'username': 'jwt_test_user',
            'password': 'ClaveSegura123!',
        }, format='json')
        self.assertEqual(token_response.status_code, 200)
        self.assertIn('access', token_response.data)
        self.assertIn('refresh', token_response.data)

        anonymous_client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {token_response.data['access']}"
        )
        products_response = anonymous_client.get('/api/products/')
        self.assertEqual(products_response.status_code, 200)
        self.assertEqual(len(products_response.data), 2)

    def test_refresh_route_returns_a_new_access_token(self):
        anonymous_client = APIClient()
        token_response = anonymous_client.post('/api/token/', {
            'username': 'jwt_test_user',
            'password': 'ClaveSegura123!',
        }, format='json')
        response = anonymous_client.post('/api/token/refresh/', {
            'refresh': token_response.data['refresh'],
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('access', response.data)

    def test_precio_final_con_token_para_dos_categorias(self):
        productos = [
            (self.mouse.pk, 'Electrónica', Decimal('225.00')),
            (Product.objects.get(name='Playera').pk, 'Ropa', Decimal('144.00')),
        ]
        for pk, categoria, total in productos:
            with self.subTest(categoria=categoria):
                response = self.client.get(f'/api/products/{pk}/precio-final/')
                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data['categoria'], categoria)
                self.assertEqual(Decimal(response.data['precio_final']), total)

    def test_precio_final_sin_token_devuelve_401(self):
        cliente_sin_token = APIClient()
        response = cliente_sin_token.get(
            f'/api/products/{self.mouse.pk}/precio-final/'
        )
        self.assertEqual(response.status_code, 401)
