# Blog de Noticias

Blog de noticias construido con Django 5.2, desplegado en Railway con PostgreSQL.

## Stack

- **Django 5.2** — framework web
- **Bootstrap 5.3** — estilos (CDN)
- **python-slugify** — slugs correctos en español
- **Pillow** — soporte de imágenes
- **WhiteNoise** — archivos estáticos en producción
- **gunicorn** — servidor WSGI de producción
- **PostgreSQL** — base de datos en producción (Railway)

## Funcionalidades

- Listado de noticias con paginación
- Detalle de noticia con noticias relacionadas
- Categorías con filtrado
- Noticia destacada (pinned en el home)
- Buscador full-text
- Archivo por mes/año
- Tiempo de lectura estimado
- SEO: meta tags y Open Graph
- Botones para compartir en redes sociales
- RSS Feed (`/feed/`)
- Sitemap XML (`/sitemap.xml`)
- Panel de administración con permisos por roles

## URLs

| URL | Descripción |
|---|---|
| `/` | Página de inicio |
| `/noticias/` | Todas las noticias |
| `/noticias/<slug>/` | Artículo completo |
| `/categoria/<slug>/` | Noticias por categoría |
| `/archivo/<año>/<mes>/` | Noticias por mes |
| `/buscar/?q=término` | Buscador |
| `/feed/` | RSS Feed |
| `/sitemap.xml` | Sitemap |
| `/admin/` | Panel de administración |

## Inicio rápido (desarrollo local)

```bash
# Clonar y entrar al directorio
git clone <repo>
cd Blog_noticias

# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```

Abrir `http://127.0.0.1:8000/` en el navegador.

## Producción

Desplegado en **Railway** con PostgreSQL. Variables de entorno requeridas:

| Variable | Descripción |
|---|---|
| `SECRET_KEY` | Clave secreta de Django |
| `DEBUG` | `False` en producción |
| `ALLOWED_HOSTS` | Dominio público de la app |
| `DATABASE_URL` | URL de PostgreSQL (Railway la provee automáticamente) |

## Documentación completa

Ver [TUTORIAL.md](TUTORIAL.md) para la guía paso a paso completa: construcción del proyecto desde cero, todos los archivos con su código, explicación de cada decisión, y el proceso completo de deploy en Railway.
