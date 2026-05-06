"""
Django settings for blog_noticias project.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── Seguridad ──────────────────────────────────────────────────────────────

# Lee la SECRET_KEY desde variable de entorno.
# En producción (Railway) se configura como variable de entorno.
# En desarrollo local usa el fallback (nunca commitear claves reales).
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-insegura-solo-para-desarrollo')

# DEBUG=False en producción. Para activar en local: setear DEBUG=True en el entorno.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Lee hosts permitidos desde env var (separados por coma) + siempre permite Railway.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS += ['.railway.app', 'radarinfo.ar', 'www.radarinfo.ar']


# ─── Aplicaciones ───────────────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'noticias',
    'django.contrib.sitemaps',
]


# ─── Middleware ─────────────────────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise debe ir inmediatamente después de SecurityMiddleware
    # para interceptar requests de archivos estáticos antes que cualquier otro middleware.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_noticias.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'noticias.context_processors.categorias_globales',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog_noticias.wsgi.application'


# ─── Base de datos ───────────────────────────────────────────────────────────
#
# dj_database_url.config() lee DATABASE_URL del entorno.
# Railway lo provee automáticamente al conectar el plugin PostgreSQL.
# Si DATABASE_URL no existe (desarrollo local) usa SQLite como fallback.

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# ─── Validación de contraseñas ───────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ─── Internacionalización ────────────────────────────────────────────────────

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True


# ─── Archivos estáticos ──────────────────────────────────────────────────────
#
# STATICFILES_DIRS: carpetas donde están los estáticos del proyecto (en desarrollo).
# STATIC_ROOT: carpeta donde collectstatic deposita todo para producción.
# WhiteNoise sirve desde STATIC_ROOT en producción sin necesidad de Nginx.

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# CompressedManifestStaticFilesStorage: comprime archivos y agrega hash al nombre
# para invalidar caché del navegador cuando cambia el contenido.
# Requiere Django 5.x — usa STORAGES dict en lugar del deprecado STATICFILES_STORAGE.
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# ─── Archivos media (imágenes subidas por usuarios) ──────────────────────────
#
# ADVERTENCIA: Railway tiene filesystem efímero.
# Los archivos subidos se pierden en cada redeploy.
# Solución futura: migrar a Cloudflare R2 o AWS S3 con django-storages.

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ─── Primary key por defecto ─────────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ─── Seguridad en producción (solo cuando DEBUG=False) ───────────────────────
#
# Railway termina SSL en su proxy y reenvía requests como HTTP interno.
# SECURE_PROXY_SSL_HEADER le dice a Django que confíe en X-Forwarded-Proto
# para detectar si la conexión original era HTTPS.

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
