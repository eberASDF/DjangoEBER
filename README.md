# APPDEWEBINTEGRALCONNOMBRECAMBIADO

API Django de tienda online con productos, categorías, usuarios con correo electrónico y JWT.

## Instalación

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Swagger: `http://127.0.0.1:8000/swagger/`.

## Rutas principales

- `POST /api/v1/auth/token/`: obtiene tokens con `email` y `password`.
- `POST /api/v1/auth/token/refresh/`: renueva el token de acceso.
- `GET /api/v1/auth/me/`: devuelve los datos personales con `Authorization: Bearer <access>`.
- `/api/v1/users/`: CRUD de usuarios, solo administradores.
- `/api/v1/products/` y `/api/v1/categories/`: recursos de la práctica anterior.

El campo extra del usuario es `telefono`. La contraseña es solo de escritura en la API. Las rutas `/api/token/` y `/api/token/refresh/` siguen disponibles para compatibilidad.
