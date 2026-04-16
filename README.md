# Blog de Noticias — Tutorial completo con Django

Guía paso a paso para construir desde cero una aplicación web de blog de noticias con Django. Sirve tanto para entender cómo está construido este proyecto como para aprender a construirlo de nuevo.

---

## Índice

1. [Requisitos previos](#1-requisitos-previos)
2. [Crear el repositorio Git](#2-crear-el-repositorio-git)
3. [Entorno virtual y dependencias](#3-entorno-virtual-y-dependencias)
4. [Crear el proyecto Django y la app](#4-crear-el-proyecto-django-y-la-app)
5. [Configurar settings.py](#5-configurar-settingspy)
6. [Definir los modelos](#6-definir-los-modelos)
7. [Migraciones](#7-migraciones)
8. [Configurar el admin](#8-configurar-el-admin)
9. [Context processor global](#9-context-processor-global)
10. [Definir las vistas](#10-definir-las-vistas)
11. [Definir las URLs](#11-definir-las-urls)
12. [RSS Feed y Sitemap](#12-rss-feed-y-sitemap)
13. [Crear los templates](#13-crear-los-templates)
14. [Estilos CSS](#14-estilos-css)
15. [Crear superusuario y cargar datos](#15-crear-superusuario-y-cargar-datos)
16. [Gestión de usuarios y permisos](#16-gestión-de-usuarios-y-permisos)
17. [Iniciar el servidor](#17-iniciar-el-servidor)
18. [Estructura final del proyecto](#18-estructura-final-del-proyecto)
19. [Referencia de URLs](#19-referencia-de-urls)

---

## 1. Requisitos previos

Antes de empezar necesitás tener instalado:

- **Python 3.10+** — verificá con `python --version`
- **pip** — viene incluido con Python
- **Git** — para el control de versiones

---

## 2. Crear el repositorio Git

Primero creamos la carpeta del proyecto e inicializamos Git.

```bash
mkdir Blog_noticias
cd Blog_noticias
git init
```

### .gitignore

Antes de hacer cualquier commit, creamos el `.gitignore` para que Git ignore archivos que no deben subirse al repositorio:

```
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python

# Entorno virtual
venv/
env/
.env/
.venv/

# Variables de entorno
.env
.env.local
*.env

# Django
*.log
db.sqlite3
media/

# Archivos estáticos recolectados (collectstatic)
staticfiles/
static_root/

# Distribución / empaquetado
dist/
build/
*.egg-info/
*.egg

# IDEs
.vscode/
.idea/
*.sublime-project
*.sublime-workspace

# Sistema operativo
.DS_Store
Thumbs.db
desktop.ini
```

**Por qué excluimos estas cosas:**
- `db.sqlite3` → es la base de datos local, contiene datos de desarrollo, no código
- `media/` → imágenes subidas por usuarios, son datos, no código fuente
- `venv/` → el entorno virtual puede recrearse con `requirements.txt`
- `.env` → puede contener contraseñas y claves secretas

### .gitattributes

Para evitar problemas de saltos de línea entre Windows (CRLF) y Linux/Mac (LF):

```
# Normalizar saltos de línea a LF en el repo para todos los archivos de texto
* text=auto eol=lf

# Archivos binarios: sin conversión
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.pdf binary
*.sqlite3 binary
```

```bash
git add .gitignore .gitattributes
git commit -m "Inicializar repositorio con gitignore y gitattributes"
```

---

## 3. Entorno virtual y dependencias

Un **entorno virtual** es una instalación de Python aislada para este proyecto. Evita conflictos entre versiones de paquetes de distintos proyectos.

```bash
# Crear el entorno virtual (se crea la carpeta venv/)
python -m venv venv

# Activar el entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate
```

Cuando el entorno está activo, el prompt muestra `(venv)` al inicio.

### Instalar dependencias

```bash
pip install django pillow python-slugify
```

- **django** → el framework web
- **pillow** → necesario para que Django maneje el campo `ImageField` (imágenes)
- **python-slugify** → convierte títulos en español a slugs URL-amigables correctamente (sin problemas con acentos y caracteres especiales)

### Guardar las dependencias

```bash
pip freeze > requirements.txt
```

O crearlo manualmente con solo las dependencias directas:

```
django
pillow
python-slugify
```

> **Para instalar en otro equipo:** `pip install -r requirements.txt`

---

## 4. Crear el proyecto Django y la app

Django tiene dos conceptos distintos:
- **Proyecto** (`blog_noticias/`) → configuración global, settings, URLs raíz
- **App** (`noticias/`) → módulo funcional con modelos, vistas y URLs propias

```bash
# Crear el proyecto (el punto "." indica que se crea en la carpeta actual)
django-admin startproject blog_noticias .

# Crear la app
python manage.py startapp noticias
```

Esto genera la siguiente estructura inicial:

```
Blog_noticias/
├── manage.py                   ← herramienta de comandos de Django
├── blog_noticias/              ← paquete de configuración del proyecto
│   ├── __init__.py
│   ├── settings.py             ← configuración global
│   ├── urls.py                 ← URLs raíz
│   ├── asgi.py
│   └── wsgi.py
└── noticias/                   ← app principal
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    ├── views.py
    └── migrations/
        └── __init__.py
```

### Crear carpetas adicionales

```bash
mkdir templates
mkdir -p static/css
mkdir media
```

---

## 5. Configurar settings.py

Abrí `blog_noticias/settings.py` y realizá los siguientes cambios:

### 5.1 Registrar la app y sitemaps

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'noticias',                     # ← nuestra app
    'django.contrib.sitemaps',      # ← para generar sitemap.xml
]
```

### 5.2 Configurar templates

Le decimos a Django que busque templates en la carpeta `templates/` de la raíz:

```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],   # ← agregar esta línea
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'noticias.context_processors.categorias_globales',  # ← nuestro processor
            ],
        },
    },
]
```

> **¿Qué es un context processor?** Es una función que se ejecuta en cada request y agrega variables al contexto de todos los templates automáticamente. Lo usamos para que las categorías estén disponibles en el navbar de todas las páginas sin tener que pasarlas desde cada vista.

### 5.3 Idioma y zona horaria

```python
LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True
```

### 5.4 Archivos estáticos y media

```python
# Archivos estáticos (CSS, JS propios del proyecto)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']   # carpeta donde están los estáticos en desarrollo

# Archivos subidos por usuarios (imágenes de noticias)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'            # carpeta donde se guardan en disco
```

**Diferencia entre static y media:**
- `static/` → archivos del desarrollador (CSS, JS, íconos). Se sirven con `{% load static %}`
- `media/` → archivos subidos por los usuarios (imágenes de noticias). Se sirven desde `MEDIA_URL`

---

## 6. Definir los modelos

Los modelos son clases Python que representan tablas en la base de datos. Django los traduce automáticamente a SQL.

Editá `noticias/models.py`:

```python
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from slugify import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre')
    slug = models.SlugField(unique=True, max_length=120)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('categoria', kwargs={'slug': self.slug})


class Noticia(models.Model):
    titulo = models.CharField(max_length=200, verbose_name='Título')
    slug = models.SlugField(unique=True, max_length=220)
    cuerpo = models.TextField(verbose_name='Contenido')
    fecha_publicacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de publicación')
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Categoría'
    )
    meta_descripcion = models.CharField(
        max_length=160,
        blank=True,
        verbose_name='Meta descripción',
        help_text='Resumen para motores de búsqueda y redes sociales (máx. 160 caracteres). Si se deja vacío se genera automáticamente.'
    )
    destacada = models.BooleanField(
        default=False,
        verbose_name='Destacada',
        help_text='Mostrar esta noticia en primer lugar en el home'
    )
    imagen_destacada = models.ImageField(
        upload_to='noticias/',
        blank=True,
        null=True,
        verbose_name='Imagen destacada'
    )

    class Meta:
        ordering = ['-fecha_publicacion']
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'

    def __str__(self):
        return self.titulo

    @property
    def tiempo_lectura(self):
        from django.utils.html import strip_tags
        palabras = len(strip_tags(self.cuerpo).split())
        return max(1, round(palabras / 200))

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('detalle_noticia', kwargs={'slug': self.slug})
```

### Explicación de los campos

| Campo | Tipo | Descripción |
|---|---|---|
| `titulo` | `CharField` | Texto corto, máximo 200 caracteres |
| `slug` | `SlugField` | URL amigable, ej: `el-dolar-cayo-hoy`. Único en la BD |
| `cuerpo` | `TextField` | Texto largo sin límite. Acepta HTML (se renderiza con `\|safe`) |
| `fecha_publicacion` | `DateTimeField` | Se establece automáticamente al crear (`auto_now_add=True`) |
| `autor` | `ForeignKey(User)` | Relación con el modelo User de Django. Si se borra el usuario, se borra la noticia (`CASCADE`) |
| `categoria` | `ForeignKey(Categoria)` | Relación opcional. Si se borra la categoría, la noticia queda sin categoría (`SET_NULL`) |
| `meta_descripcion` | `CharField` | Opcional. Para SEO y Open Graph. Si está vacío se genera del cuerpo |
| `destacada` | `BooleanField` | Si es `True`, aparece primero y más grande en el home |
| `imagen_destacada` | `ImageField` | Imagen opcional. Se guarda en `media/noticias/` |

### Conceptos clave

**`slug`** es un identificador en la URL limpio de caracteres especiales:
```
Título:  "El dólar perforó los $1.400"
Slug:    "el-dolar-perforo-los-1-400"
URL:     /noticias/el-dolar-perforo-los-1-400/
```

**`python-slugify`** maneja correctamente el español. El método `save()` genera el slug automáticamente si no se proporciona uno.

**`@property`** en `tiempo_lectura` hace que se pueda usar como atributo (`noticia.tiempo_lectura`) sin ser un campo de la base de datos. Calcula ~200 palabras por minuto.

**`get_absolute_url()`** devuelve la URL del objeto. Permite usar `{{ noticia.get_absolute_url }}` en los templates.

---

## 7. Migraciones

Las migraciones son archivos que registran los cambios en los modelos y los aplican a la base de datos.

```bash
# Crear los archivos de migración (analiza los modelos y genera el SQL)
python manage.py makemigrations

# Aplicar las migraciones (ejecuta el SQL en la base de datos)
python manage.py migrate
```

**Cuándo correr `makemigrations`:** cada vez que agregás, modificás o eliminás un campo en un modelo.

**Cuándo correr `migrate`:** después de cada `makemigrations`, y también al clonar el proyecto por primera vez.

Verificá que todo esté bien:
```bash
python manage.py check
# Debe responder: System check identified no issues (0 silenced).
```

---

## 8. Configurar el admin

El admin de Django es un panel de administración generado automáticamente. Editá `noticias/admin.py`:

```python
from django.contrib import admin
from .models import Categoria, Noticia


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'slug')
    prepopulated_fields = {'slug': ('nombre',)}


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'autor', 'fecha_publicacion', 'destacada')
    list_filter = ('fecha_publicacion', 'categoria', 'autor', 'destacada')
    search_fields = ('titulo', 'cuerpo')
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'fecha_publicacion'
    readonly_fields = ('fecha_publicacion',)
    fieldsets = (
        (None, {'fields': ('titulo', 'slug', 'categoria', 'autor', 'imagen_destacada', 'destacada')}),
        ('Contenido', {'fields': ('cuerpo',)}),
        ('SEO', {'fields': ('meta_descripcion',), 'classes': ('collapse',)}),
        ('Fechas', {'fields': ('fecha_publicacion',)}),
    )
```

### Explicación de las opciones del admin

| Opción | Efecto |
|---|---|
| `list_display` | Columnas visibles en el listado |
| `list_filter` | Panel lateral de filtros |
| `search_fields` | Habilita la búsqueda por esos campos |
| `prepopulated_fields` | El campo `slug` se rellena en tiempo real mientras escribís el título |
| `date_hierarchy` | Navegación por año/mes/día en la parte superior |
| `readonly_fields` | Campos que no se pueden editar (la fecha la pone Django automáticamente) |
| `fieldsets` | Organiza el formulario en secciones. `'classes': ('collapse',)` hace que la sección SEO empiece plegada |

---

## 9. Context processor global

Un context processor es una función que inyecta variables en el contexto de **todos** los templates, sin importar qué vista los renderice. Lo usamos para que las categorías estén disponibles en el navbar en todas las páginas.

Creá el archivo `noticias/context_processors.py`:

```python
from .models import Categoria


def categorias_globales(request):
    return {'categorias_nav': Categoria.objects.all()}
```

Esta función recibe el `request` y devuelve un diccionario. Django mezcla ese diccionario con el contexto de cada template. Así, en cualquier template podés usar `{{ categorias_nav }}` sin necesidad de pasarlo desde la vista.

Ya registramos este processor en `settings.py` en el paso 5.

---

## 10. Definir las vistas

Las vistas reciben un request HTTP y devuelven una respuesta (generalmente un template renderizado). Usamos **Class-Based Views** (vistas basadas en clases) que Django provee para casos comunes.

Editá `noticias/views.py`:

```python
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Noticia, Categoria


class HomeView(ListView):
    model = Noticia
    template_name = 'home.html'
    context_object_name = 'noticias'

    def get_queryset(self):
        # Si hay una noticia destacada, va primero; el resto completa hasta 5
        destacadas = list(Noticia.objects.filter(destacada=True)[:1])
        ids_excluir = [n.pk for n in destacadas]
        recientes = list(Noticia.objects.exclude(pk__in=ids_excluir)[:5 - len(destacadas)])
        return destacadas + recientes

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class ListaNoticiasView(ListView):
    model = Noticia
    template_name = 'lista_noticias.html'
    context_object_name = 'noticias'
    paginate_by = 10    # Django pagina automáticamente, agrega page_obj al contexto

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        return context


class DetalleNoticiaView(DetailView):
    model = Noticia
    template_name = 'detalle_noticia.html'
    context_object_name = 'noticia'
    slug_field = 'slug'         # campo del modelo que actúa como identificador
    slug_url_kwarg = 'slug'     # nombre del parámetro en la URL

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        noticia = self.object
        # Noticias relacionadas: misma categoría, o mismo mes si no tiene categoría
        if noticia.categoria:
            relacionadas = Noticia.objects.filter(
                categoria=noticia.categoria
            ).exclude(pk=noticia.pk)[:3]
        else:
            relacionadas = Noticia.objects.filter(
                fecha_publicacion__year=noticia.fecha_publicacion.year,
                fecha_publicacion__month=noticia.fecha_publicacion.month,
            ).exclude(pk=noticia.pk)[:3]
        context['relacionadas'] = relacionadas
        return context


class CategoriaView(ListView):
    model = Noticia
    template_name = 'lista_noticias.html'   # reutiliza el mismo template
    context_object_name = 'noticias'
    paginate_by = 10

    def get_queryset(self):
        # Guardamos la categoría para usarla en get_context_data
        self.categoria = Categoria.objects.get(slug=self.kwargs['slug'])
        return Noticia.objects.filter(categoria=self.categoria)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categoria_activa'] = self.categoria
        context['categorias'] = Categoria.objects.all()
        return context


class NoticiasPorFechaView(ListView):
    model = Noticia
    template_name = 'archivo_fecha.html'
    context_object_name = 'noticias'
    paginate_by = 10

    def get_queryset(self):
        anio = self.kwargs['anio']
        mes = self.kwargs['mes']
        return Noticia.objects.filter(
            fecha_publicacion__year=anio,
            fecha_publicacion__month=mes,
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['anio'] = self.kwargs['anio']
        context['mes'] = self.kwargs['mes']
        context['categorias'] = Categoria.objects.all()
        return context


class BuscadorView(ListView):
    template_name = 'buscar.html'
    context_object_name = 'noticias'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        if q:
            # Q() permite combinar condiciones con OR (|) o AND (&)
            return Noticia.objects.filter(
                Q(titulo__icontains=q) | Q(cuerpo__icontains=q)
            )
        return Noticia.objects.none()   # queryset vacío si no hay término

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


# Convertir las clases en funciones de vista (necesario para urls.py)
home = HomeView.as_view()
lista_noticias = ListaNoticiasView.as_view()
detalle_noticia = DetalleNoticiaView.as_view()
categoria = CategoriaView.as_view()
noticias_por_fecha = NoticiasPorFechaView.as_view()
buscar = BuscadorView.as_view()
```

### Class-Based Views: conceptos clave

| Clase base | Para qué sirve |
|---|---|
| `ListView` | Mostrar una lista de objetos. Provee `paginate_by` automático |
| `DetailView` | Mostrar un objeto específico buscado por `pk` o `slug` |

**`get_queryset()`** → define qué objetos se obtienen de la BD. Por defecto devuelve todos.

**`get_context_data()`** → agrega variables extra al contexto del template. Siempre llamar a `super()` primero.

**`self.kwargs`** → parámetros capturados de la URL (ej: `<int:anio>` → `self.kwargs['anio']`).

**`icontains`** → búsqueda case-insensitive que ignora mayúsculas/minúsculas.

---

## 11. Definir las URLs

### URLs de la app (`noticias/urls.py`)

Creá el archivo `noticias/urls.py`:

```python
from django.urls import path
from . import views
from .feeds import UltimasNoticiasFeed

urlpatterns = [
    path('', views.home, name='home'),
    path('noticias/', views.lista_noticias, name='lista_noticias'),
    path('noticias/<slug:slug>/', views.detalle_noticia, name='detalle_noticia'),
    path('categoria/<slug:slug>/', views.categoria, name='categoria'),
    path('archivo/<int:anio>/<int:mes>/', views.noticias_por_fecha, name='noticias_por_fecha'),
    path('buscar/', views.buscar, name='buscar'),
    path('feed/', UltimasNoticiasFeed(), name='feed'),
]
```

**Convertidores de URL:**
- `<slug:slug>` → acepta letras, números y guiones. Ej: `el-dolar-cayo`
- `<int:anio>` → acepta solo números enteros. Ej: `2026`

El parámetro `name=` permite referenciar la URL desde templates con `{% url 'home' %}` en lugar de hardcodear la ruta.

### URLs del proyecto (`blog_noticias/urls.py`)

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from noticias.sitemaps import NoticiasSitemap

sitemaps = {
    'noticias': NoticiasSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('', include('noticias.urls')),   # incluye todas las URLs de la app
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ^ esto sirve los archivos media en desarrollo (DEBUG=True)
```

**`include()`** → delega las URLs al archivo `noticias/urls.py`. Mantiene el proyecto organizado.

---

## 12. RSS Feed y Sitemap

### RSS Feed (`noticias/feeds.py`)

```python
from django.contrib.syndication.views import Feed
from django.utils.html import strip_tags
from .models import Noticia


class UltimasNoticiasFeed(Feed):
    title = 'Blog de Noticias'
    link = '/noticias/'
    description = 'Últimas noticias publicadas.'

    def items(self):
        return Noticia.objects.all()[:20]

    def item_title(self, item):
        return item.titulo

    def item_description(self, item):
        return strip_tags(item.cuerpo)[:300]   # texto plano, sin HTML

    def item_pubdate(self, item):
        return item.fecha_publicacion

    def item_author_name(self, item):
        return item.autor.get_full_name() or item.autor.username
```

El RSS es un formato XML estándar que permite a los lectores de noticias suscribirse al blog. Disponible en `/feed/`.

### Sitemap (`noticias/sitemaps.py`)

```python
from django.contrib.sitemaps import Sitemap
from .models import Noticia


class NoticiasSitemap(Sitemap):
    changefreq = 'daily'    # frecuencia de actualización sugerida a Google
    priority = 0.8          # prioridad relativa (0.0 a 1.0)

    def items(self):
        return Noticia.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion
```

El sitemap en `/sitemap.xml` le indica a Google qué páginas indexar y cuándo se actualizaron por última vez.

---

## 13. Crear los templates

Los templates son archivos HTML con sintaxis de Django (`{% %}` para lógica, `{{ }}` para variables).

### Estructura de templates

```
templates/
├── base.html           ← plantilla base con navbar y footer
├── home.html           ← página de inicio
├── lista_noticias.html ← listado completo (también usado para categorías)
├── detalle_noticia.html← artículo completo
├── archivo_fecha.html  ← filtrado por mes/año
└── buscar.html         ← resultados de búsqueda
```

### Herencia de templates

El sistema de herencia evita repetir el HTML del navbar y footer en cada página:

```
base.html
├── home.html          ({% extends 'base.html' %})
├── lista_noticias.html
├── detalle_noticia.html
├── archivo_fecha.html
└── buscar.html
```

En `base.html` se definen bloques con `{% block nombre %}{% endblock %}`. Cada template hijo los rellena con `{% block nombre %}contenido{% endblock %}`.

### Filtros de template más usados en este proyecto

| Filtro | Ejemplo | Resultado |
|---|---|---|
| `striptags` | `{{ cuerpo\|striptags }}` | Elimina etiquetas HTML |
| `truncatewords:N` | `{{ texto\|truncatewords:20 }}` | Corta en N palabras |
| `safe` | `{{ cuerpo\|safe }}` | Renderiza HTML sin escapar |
| `date:"d/m/Y"` | `{{ fecha\|date:"d/m/Y" }}` | Formatea la fecha |
| `urlencode` | `{{ url\|urlencode }}` | Codifica para usar en URLs |
| `default:valor` | `{{ campo\|default:"Sin nombre" }}` | Valor si el campo está vacío |

> **Nota sobre `|safe`:** el cuerpo de las noticias se escribe como HTML (generado por Gemini). El filtro `|safe` le indica a Django que no escape las etiquetas. Solo usarlo con contenido de confianza (escrito por administradores).

---

## 14. Estilos CSS

El proyecto usa **Bootstrap 5** cargado desde CDN y un archivo de estilos propios en `static/css/estilos.css`.

Para cargar archivos estáticos propios en un template, hay que incluir al inicio:

```html
{% load static %}
...
<link rel="stylesheet" href="{% static 'css/estilos.css' %}">
```

`{% load static %}` carga el tag `{% static %}` que resuelve la URL correcta del archivo.

### Estilos para tablas dentro del cuerpo HTML

Como el cuerpo de las noticias es HTML libre, los estilos de tablas se aplican con CSS apuntando al contenedor `.noticia-cuerpo table`, sin necesidad de agregar clases al HTML generado por Gemini:

```css
.noticia-cuerpo table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
}

.noticia-cuerpo table th {
  background-color: #212529;
  color: #fff;
}
```

---

## 15. Crear superusuario y cargar datos

Para acceder al panel de administración y crear noticias:

```bash
python manage.py createsuperuser
```

Django pedirá:
- Nombre de usuario
- Email (opcional)
- Contraseña (mínimo 8 caracteres)

---

## 16. Gestión de usuarios y permisos

Django tiene un sistema de permisos integrado. Cada modelo genera automáticamente 4 permisos: `add`, `change`, `delete` y `view`. El enfoque recomendado es crear un **Grupo** con los permisos necesarios y asignar usuarios a ese grupo, en lugar de configurar permisos uno por uno.

### Tipos de usuario en Django

| Tipo | `is_staff` | `is_superuser` | Acceso |
|---|---|---|---|
| **Superusuario** | ✅ | ✅ | Admin completo, sin restricciones |
| **Staff / Redactor** | ✅ | ❌ | Accede al admin solo con los permisos que se le asignen |
| **Usuario regular** | ❌ | ❌ | No accede al admin |

> La clave es `is_staff = True`: sin esto, el usuario no puede ingresar a `/admin/` aunque tenga permisos asignados.

---

### Paso 1 — Crear el grupo "Redactores"

Los grupos permiten asignar el mismo conjunto de permisos a varios usuarios a la vez. Si después necesitás cambiar los permisos del rol, lo cambiás en el grupo y afecta a todos los usuarios de ese grupo.

1. Ir a `http://127.0.0.1:8000/admin/`
2. En el menú lateral → **Autenticación y Autorización** → **Grupos**
3. Click en **Añadir grupo**
4. Nombre: `Redactores`
5. En el panel de permisos disponibles, buscar `noticia` y seleccionar:
   - `noticias | noticia | Can add noticia` ✅
   - `noticias | noticia | Can change noticia` ✅
   - `noticias | noticia | Can view noticia` ✅
   - `noticias | noticia | Can delete noticia` ← opcional, solo si querés que puedan borrar
6. También agregar permisos de categoría si deben poder crearlas:
   - `noticias | categoría | Can add categoría` ✅
   - `noticias | categoría | Can change categoría` ✅
   - `noticias | categoría | Can view categoría` ✅
7. Usar la flecha **→** para moverlos al panel de "Permisos elegidos"
8. Click en **Guardar**

---

### Paso 2 — Crear un nuevo usuario

1. En el admin → **Autenticación y Autorización** → **Usuarios**
2. Click en **Añadir usuario**
3. Completar **Nombre de usuario** y **Contraseña** → click en **Guardar y continuar editando**
4. En la siguiente pantalla configurar:
   - **Nombre** y **Apellidos** (opcionales, pero aparecen como autor en las noticias)
   - **Dirección de correo electrónico** (opcional)
   - En la sección **Permisos**:
     - Tildar **"El usuario puede acceder al sitio de administración"** (`is_staff`) ← **obligatorio**
     - NO tildar "Es superusuario"
   - En la sección **Grupos**: seleccionar `Redactores` y moverlo con la flecha **→**
5. Click en **Guardar**

---

### Paso 3 — Verificar el acceso

El nuevo usuario debería poder:

| Acción | ¿Puede? |
|---|---|
| Ingresar a `/admin/` | ✅ |
| Ver listado de noticias | ✅ |
| Crear noticias | ✅ |
| Editar noticias | ✅ |
| Eliminar noticias | Solo si se le dio ese permiso |
| Ver/crear categorías | Solo si se le dio ese permiso |
| Ver/crear usuarios | ❌ |
| Cambiar configuración del sitio | ❌ |

> El redactor solo ve en su admin las secciones para las que tiene permisos. No ve usuarios ni grupos.

---

### Resumen visual del sistema de permisos

```
Superusuario
└── Acceso total a todo el admin

Grupo: Redactores
├── noticias | noticia | add
├── noticias | noticia | change
├── noticias | noticia | view
└── noticias | categoría | view

Usuario "juan" (is_staff=True)
└── Grupos: [Redactores]
    └── Hereda todos los permisos del grupo
```

---

### Cambiar permisos de un usuario existente

- **Para darle más permisos:** agregarlo a otro grupo, o asignarle permisos individuales desde su perfil en el admin en la sección "Permisos de usuario"
- **Para quitarle el acceso temporalmente:** destildar `is_staff` en su perfil (sigue existiendo el usuario pero no puede entrar al admin)
- **Para cambiar el rol de todos los redactores:** editar el grupo `Redactores` y los cambios se aplican automáticamente a todos sus miembros

---

## 17. Iniciar el servidor

```bash
python manage.py runserver
```

El servidor de desarrollo queda corriendo en `http://127.0.0.1:8000/`.

Para detenerlo: `Ctrl + C`

### Flujo de trabajo recomendado para cargar noticias

1. Ir a `http://127.0.0.1:8000/admin/`
2. Crear las **Categorías** primero (Economía, Política, Tecnología, etc.)
3. Crear **Noticias**: el `slug` se auto-completa desde el título
4. Pegar el HTML generado por Gemini en el campo **Contenido**
5. Asignar categoría e imagen destacada
6. Guardar y verificar en `http://127.0.0.1:8000/`

---

## 18. Estructura final del proyecto

```
Blog_noticias/
├── .gitignore
├── .gitattributes
├── manage.py
├── requirements.txt
├── db.sqlite3                          ← base de datos (no se commitea)
│
├── blog_noticias/                      ← configuración del proyecto
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── noticias/                           ← app principal
│   ├── models.py                       ← Categoria + Noticia
│   ├── views.py                        ← 6 vistas (Home, Lista, Detalle, Categoria, Fecha, Buscar)
│   ├── urls.py                         ← 7 rutas + feed RSS
│   ├── admin.py                        ← panel de administración
│   ├── context_processors.py           ← categorías en todas las páginas
│   ├── feeds.py                        ← RSS Feed
│   ├── sitemaps.py                     ← Sitemap XML
│   └── migrations/                     ← historial de cambios en la BD
│
├── templates/                          ← HTML
│   ├── base.html
│   ├── home.html
│   ├── lista_noticias.html
│   ├── detalle_noticia.html
│   ├── archivo_fecha.html
│   └── buscar.html
│
├── static/                             ← archivos del desarrollador
│   └── css/
│       └── estilos.css
│
└── media/                              ← imágenes subidas (no se commitea)
    └── noticias/
```

---

## 19. Referencia de URLs

| URL | Vista | Descripción |
|---|---|---|
| `/` | `HomeView` | Página de inicio: 1 destacada + 4 recientes |
| `/noticias/` | `ListaNoticiasView` | Todas las noticias, paginadas (10/página) |
| `/noticias/<slug>/` | `DetalleNoticiaView` | Artículo completo |
| `/categoria/<slug>/` | `CategoriaView` | Noticias filtradas por categoría |
| `/archivo/<año>/<mes>/` | `NoticiasPorFechaView` | Noticias de un mes específico |
| `/buscar/?q=término` | `BuscadorView` | Resultados de búsqueda |
| `/feed/` | `UltimasNoticiasFeed` | RSS Feed (XML) |
| `/sitemap.xml` | Django sitemaps | Sitemap para Google |
| `/admin/` | Django admin | Panel de administración |

---

## Comandos de referencia rápida

```bash
# Activar entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones después de cambiar un modelo
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar que no haya errores de configuración
python manage.py check

# Crear superusuario
python manage.py createsuperuser

# Iniciar el servidor de desarrollo
python manage.py runserver

# Ver todas las URLs registradas
python manage.py show_urls      # requiere django-extensions

# Shell interactivo de Django (para probar queries)
python manage.py shell
```

### Ejemplos de queries en el shell de Django

```python
python manage.py shell

# Importar modelos
from noticias.models import Noticia, Categoria

# Obtener todas las noticias
Noticia.objects.all()

# Filtrar por categoría
Noticia.objects.filter(categoria__nombre='Economía')

# Obtener la más reciente
Noticia.objects.first()

# Buscar en el título (case-insensitive)
Noticia.objects.filter(titulo__icontains='dólar')

# Contar noticias
Noticia.objects.count()
```

---

*Proyecto construido con Django 5.2 · Bootstrap 5.3 · python-slugify · Pillow*
