# APPDEWEBINTEGRALCONNOMBRECAMBIADO

Proyecto de la segunda actividad: backend Django REST Framework con JWT y frontend React con Vite. Conserva el CRUD de productos y categorías de la primera unidad. El sitio presenta un archivo visual inspirado en el universo Avatar, con imágenes de personajes de una API pública y una consulta SOAP desde Django.

## Requisitos

- Python 3.12 o superior
- Node.js 20 o superior
- Conexión a Internet para consultar la API pública de Avatar y el servicio SOAP

## Backend

En PowerShell, desde la raíz del repositorio:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

La [Last Airbender API](https://github.com/paigeegorry/last-airbender-api) es pública y no requiere clave. Django consulta la API y devuelve al frontend los nombres y las URL de las imágenes.

## Frontend

En otra terminal:

```powershell
cd frontend
npm install
npm run dev
```

Abre `http://127.0.0.1:5173`. Vite redirige `/api/` al backend local, así que no hace falta abrir CORS a todos los orígenes. En un despliegue con dominios separados configura `VITE_API_BASE_URL` y una política CORS limitada al dominio real.

## Rutas

| Ruta | Función |
| --- | --- |
| `/` | Portada pública |
| `/login` | Login con JWT |
| `/register` | Registro público |
| `/dashboard` | Pantalla protegida con usuario, imágenes externas y SOAP |
| `POST /api/v1/auth/register/` | Crear una cuenta sin privilegios |
| `POST /api/v1/auth/token/` | Obtener el token JWT |
| `GET /api/v1/auth/me/` | Datos del usuario autenticado |
| `GET /api/v1/external/avatar-scenes/` | Imágenes de personajes de Avatar, protegidas por JWT |
| `GET /api/v1/external/soap/capital/?pais=MX` | Consulta SOAP con zeep, protegida por JWT |
| `/api/v1/users/` | CRUD de usuarios, solo administradores |
| `/api/v1/products/` y `/api/v1/categories/` | Recursos existentes |
| `/swagger/` | Documentación de la API |

El widget muestra personajes de *Avatar: The Last Airbender* y *The Legend of Korra*. El botón «Cambiar imagen» recorre las imágenes devueltas. Esta API ofrece retratos de personajes; no ofrece escenas de episodios ni material de *Avatar: Seven Havens*.

El endpoint SOAP consume [CountryInfoService](http://webservices.oorsprong.org/websamples.countryinfo/CountryInfoService.wso?WSDL) con `zeep`. La consulta de ejemplo `pais=MX` devuelve la capital de México.

## Diseño y atribuciones

La composición abierta, el uso de imágenes a ancho completo y el ritmo editorial toman como referencia la [plantilla existente Nature-inspired visual essay de Figma](https://www.figma.com/community/file/1494802487063033242/nature-inspired-visual-essay). El diseño del frontend se adaptó a React y CSS, sin imágenes generadas por IA ni tarjetas. Los símbolos de los elementos son caracteres tipográficos y formas CSS.

Las imágenes que devuelve la API se alojan en Avatar Wiki. La interfaz identifica la fuente y enlaza al proyecto público de la API.

Repositorio de entrega: [github.com/eberASDF/DjangoEBER](https://github.com/eberASDF/DjangoEBER). Los archivos están preparados localmente; el propietario realizará la subida.

## Pruebas

```powershell
python manage.py test products users integrations
cd frontend
npm run build
```
