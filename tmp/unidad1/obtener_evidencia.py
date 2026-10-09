import json
import os
import secrets
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tienda_online.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from products.models import Product

root = Path(__file__).resolve().parent
username = 'unidad1_evidencia_temporal'
password = secrets.token_urlsafe(24)
user = get_user_model().objects.create_user(username=username, password=password)

def fetch(url, method='GET', data=None, token=None):
    headers = {'Accept': 'application/json'}
    body = None
    if data is not None:
        body = json.dumps(data).encode()
        headers['Content-Type'] = 'application/json'
    if token:
        headers['Authorization'] = 'Bearer ' + token
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        return response.status, json.load(response)

try:
    base = 'http://127.0.0.1:8000'
    status, tokens = fetch(base + '/api/token/', 'POST', {
        'username': username, 'password': password,
    })
    results = []
    for name in ('Mouse', 'Playera'):
        product = Product.objects.get(name=name)
        url = f'{base}/api/products/{product.pk}/precio-final/'
        code, response = fetch(url, token=tokens['access'])
        results.append({'url': url, 'status': code, 'response': response})
    (root / 'respuestas_api.json').write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8'
    )
    print(json.dumps(results, ensure_ascii=False, indent=2))
finally:
    user.delete()
