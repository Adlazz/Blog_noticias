# Tutorial completo — Blog de Noticias con Django

Guía paso a paso para construir desde cero y desplegar en producción una aplicación web de blog de noticias con Django. Sirve tanto para entender cómo está construido este proyecto como para volver a hacerlo o tomarlo de referencia para otros proyectos.

---

## Índice

**Desarrollo**
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

**Deploy en Railway**

20. [Preparar el proyecto para producción](#20-preparar-el-proyecto-para-producción)
21. [Archivos de configuración de Railway](#21-archivos-de-configuración-de-railway)
22. [Crear el proyecto en Railway](#22-crear-el-proyecto-en-railway)
23. [Agregar PostgreSQL](#23-agregar-postgresql)
24. [Configurar variables de entorno](#24-configurar-variables-de-entorno)
25. [Crear superusuario en producción](#25-crear-superusuario-en-producción)
26. [Verificación final](#26-verificación-final)
27. [Limitación conocida: archivos media](#27-limitación-conocida-archivos-media)
28. [Comandos de referencia rápida](#28-comandos-de-referencia-rápida)

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

Crear `requirements.txt` manualmente con solo las dependencias directas:

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
| `readonly_fields` | Campos que no se pueden editar |
| `fieldsets` | Organiza el formulario en secciones. `'classes': ('collapse',)` hace que la sección empiece plegada |

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
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

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

El parámetro `name=` permite referenciar la URL desde templates con `{% url 'home' %}`.

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
    path('', include('noticias.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# ^ esto sirve los archivos media en desarrollo (DEBUG=True)
```

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

> **Nota sobre `|safe`:** el cuerpo de las noticias se escribe como HTML. El filtro `|safe` le indica a Django que no escape las etiquetas. Solo usarlo con contenido de confianza (escrito por administradores).

> **Truco para excerpts en listados:** usar `{{ noticia.cuerpo|striptags|truncatewords:30 }}` para mostrar un resumen limpio sin etiquetas HTML.

---

## 14. Estilos CSS

El proyecto usa **Bootstrap 5** cargado desde CDN y un archivo de estilos propios en `static/css/estilos.css`.

Para cargar archivos estáticos propios en un template:

```html
{% load static %}
...
<link rel="stylesheet" href="{% static 'css/estilos.css' %}">
```

### Estilos para tablas dentro del cuerpo HTML

Como el cuerpo de las noticias es HTML libre, los estilos de tablas se aplican con CSS apuntando al contenedor `.noticia-cuerpo table`:

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

### Truco: evitar `<a>` anidados

En los listados de noticias, si usás `<a class="list-group-item">` como contenedor y después ponés un badge de categoría con otro `<a>`, el HTML queda inválido (ancla dentro de ancla). El navegador lo rompe creando elementos vacíos.

**Solución:** reemplazar el `<a>` contenedor externo por un `<div>` con la misma clase, y hacer que el título sea el enlace:

```html
<!-- MAL: ancla dentro de ancla -->
<a class="list-group-item" href="{{ noticia.get_absolute_url }}">
    <a class="badge" href="{{ noticia.categoria.get_absolute_url }}">Categoría</a>
</a>

<!-- BIEN: div contenedor, el título es el enlace -->
<div class="list-group-item noticia-list-item">
    <a class="badge" href="{{ noticia.categoria.get_absolute_url }}">Categoría</a>
    <h5><a href="{{ noticia.get_absolute_url }}">{{ noticia.titulo }}</a></h5>
</div>
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

### Flujo de trabajo para cargar noticias

1. Ir a `http://127.0.0.1:8000/admin/`
2. Crear las **Categorías** primero (Economía, Política, Tecnología, etc.)
3. Crear **Noticias**: el `slug` se auto-completa desde el título
4. Pegar el HTML en el campo **Contenido**
5. Asignar categoría e imagen destacada
6. Guardar y verificar en `http://127.0.0.1:8000/`

---

## 16. Gestión de usuarios y permisos

Django tiene un sistema de permisos integrado. Cada modelo genera automáticamente 4 permisos: `add`, `change`, `delete` y `view`. El enfoque recomendado es crear un **Grupo** con los permisos necesarios y asignar usuarios a ese grupo.

### Tipos de usuario en Django

| Tipo | `is_staff` | `is_superuser` | Acceso |
|---|---|---|---|
| **Superusuario** | ✅ | ✅ | Admin completo, sin restricciones |
| **Staff / Redactor** | ✅ | ❌ | Accede al admin solo con los permisos que se le asignen |
| **Usuario regular** | ❌ | ❌ | No accede al admin |

> La clave es `is_staff = True`: sin esto, el usuario no puede ingresar a `/admin/` aunque tenga permisos asignados.

### Paso 1 — Crear el grupo "Redactores"

1. Ir a `/admin/` → **Autenticación y Autorización** → **Grupos**
2. Click en **Añadir grupo** → Nombre: `Redactores`
3. Seleccionar los permisos de noticia: `add`, `change`, `view` (y `delete` si corresponde)
4. Opcionalmente agregar permisos de categoría
5. Guardar

### Paso 2 — Crear un nuevo usuario

1. Admin → **Usuarios** → **Añadir usuario**
2. Completar username y contraseña → **Guardar y continuar editando**
3. Tildar **"El usuario puede acceder al sitio de administración"** (`is_staff`) — obligatorio
4. En la sección **Grupos**: seleccionar `Redactores`
5. Guardar

### Resumen del sistema de permisos

```
Superusuario
└── Acceso total a todo el admin

Grupo: Redactores
├── noticias | noticia | add
├── noticias | noticia | change
└── noticias | noticia | view

Usuario "juan" (is_staff=True)
└── Grupos: [Redactores]
    └── Hereda todos los permisos del grupo
```

---

## 17. Iniciar el servidor

```bash
python manage.py runserver
```

El servidor de desarrollo queda corriendo en `http://127.0.0.1:8000/`.

Para detenerlo: `Ctrl + C`

---

## 18. Estructura final del proyecto

```
Blog_noticias/
├── .gitignore
├── .gitattributes
├── manage.py
├── requirements.txt
├── Procfile                            ← comando de inicio para Railway
├── railway.toml                        ← configuración de build y deploy
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

---

# Deploy en Railway

Esta sección cubre cómo llevar el proyecto de desarrollo local a producción en **Railway** con **PostgreSQL**. Los pasos son independientes de la parte de desarrollo y se pueden aplicar a cualquier proyecto Django similar.

---

## 20. Preparar el proyecto para producción

El `settings.py` de desarrollo no sirve para producción. Hay que hacerlo seguro y flexible mediante variables de entorno.

### 20.1 Dependencias adicionales

Agregar al `requirements.txt`:

```
django
pillow
python-slugify
gunicorn          ← servidor WSGI de producción (reemplaza runserver)
psycopg2-binary   ← driver de PostgreSQL
whitenoise        ← sirve archivos estáticos sin necesidad de Nginx
dj-database-url   ← parsea DATABASE_URL del entorno
```

### 20.2 settings.py para producción

Reemplazar el `settings.py` de desarrollo con esta versión preparada para producción:

```python
import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECRET_KEY desde variable de entorno (nunca hardcodeada)
SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-local-insegura-solo-para-desarrollo')

# DEBUG=False en producción. Para activar en local: setear DEBUG=True en el entorno.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Hosts permitidos desde env var + siempre permite Railway
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
ALLOWED_HOSTS += ['.railway.app']

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # ← segunda posición, siempre
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

# dj_database_url.config() lee DATABASE_URL del entorno.
# Railway lo provee automáticamente al conectar el plugin PostgreSQL.
# Si DATABASE_URL no existe (desarrollo local) usa SQLite como fallback.
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'   # ← donde collectstatic deposita todo

# CompressedManifestStaticFilesStorage: comprime archivos y agrega hash al nombre
# para invalidar caché del navegador. Requiere Django 5.x — usa STORAGES dict.
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Seguridad HTTPS solo cuando DEBUG=False
# Railway termina SSL en su proxy y reenvía requests como HTTP interno.
# SECURE_PROXY_SSL_HEADER le dice a Django que confíe en X-Forwarded-Proto.
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
```

### Por qué cada cambio

| Cambio | Razón |
|---|---|
| `SECRET_KEY` desde env var | Nunca commitear claves secretas al repositorio |
| `DEBUG` desde env var | En producción debe ser `False` para no exponer tracebacks |
| `ALLOWED_HOSTS` desde env var | Railway rechaza requests si el host no está permitido |
| WhiteNoise en MIDDLEWARE | Sirve archivos estáticos sin Nginx, en segunda posición obligatoria |
| `dj_database_url` | Lee `DATABASE_URL` que Railway provee automáticamente con PostgreSQL |
| `STATIC_ROOT` | `collectstatic` necesita saber dónde depositar los archivos |
| `STORAGES` con CompressedManifest | Comprime y versiona los estáticos para mejor caché |
| Bloque HTTPS | Railway usa proxy SSL — Django necesita este header para detectar HTTPS |

---

## 21. Archivos de configuración de Railway

### `Procfile`

Crear en la raíz del proyecto:

```
web: gunicorn blog_noticias.wsgi --log-file -
```

Railway detecta este archivo y lo usa como comando de inicio. `--log-file -` envía los logs al stdout para que Railway los capture.

### `railway.toml`

Crear en la raíz del proyecto:

```toml
[build]
builder = "nixpacks"
buildCommand = "pip install -r requirements.txt && python manage.py collectstatic --noinput"

[deploy]
startCommand = "python manage.py migrate && gunicorn blog_noticias.wsgi --log-file -"
restartPolicyType = "on_failure"
```

- **buildCommand** → se ejecuta una sola vez al deployar. Instala deps y recolecta estáticos.
- **startCommand** → se ejecuta al iniciar el contenedor. Aplica migraciones y arranca gunicorn.
- `--noinput` → collectstatic no pide confirmación en CI.

### Commit de estos cambios

```bash
git add requirements.txt blog_noticias/settings.py Procfile railway.toml
git commit -m "chore: configure project for Railway deployment"
git push origin main
```

---

## 22. Crear el proyecto en Railway

1. Ir a [railway.app](https://railway.app) → **New Project**
2. Seleccionar **"Deploy from GitHub repo"**
3. Conectar la cuenta de GitHub si es la primera vez
4. Seleccionar el repositorio del proyecto
5. Railway detecta automáticamente que es un proyecto Python/Django y empieza el primer deploy

---

## 23. Agregar PostgreSQL

En el canvas del proyecto (vista principal con los bloques de servicios):

1. Click en **"+ Add"** (esquina superior derecha) o click derecho en el canvas vacío
2. Seleccionar **"Database"** → **"Add PostgreSQL"**
3. Railway crea el servicio Postgres y lo vincula al proyecto

`DATABASE_URL` queda disponible como variable interna de Railway.

---

## 24. Configurar variables de entorno

En el panel de **Blog_noticias** → pestaña **Variables** → **+ New Variable**:

| Variable | Valor |
|---|---|
| `SECRET_KEY` | Generar con: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"` |
| `DEBUG` | `False` |
| `ALLOWED_HOSTS` | `tu-app.up.railway.app` (el dominio que Railway asigna) |
| `DATABASE_URL` | `${{Postgres.DATABASE_URL}}` (referencia interna de Railway) |

> **Dónde obtener el dominio:** Blog_noticias → Settings → Networking → **Generate Domain** → copiar el dominio generado.

> **`${{Postgres.DATABASE_URL}}`** es una referencia de Railway que se resuelve automáticamente al valor real de conexión de la base de datos. No es necesario copiar manualmente la URL de PostgreSQL.

Al guardar las variables, Railway re-deployará automáticamente con la nueva configuración.

---

## 25. Crear superusuario en producción

Una vez que el deploy está en verde (**Deployment successful**), hay que crear el superusuario en la base de datos de producción.

### Instalar Railway CLI

```bash
npm install -g @railway/cli
```

### Conectar al contenedor

En Railway: click derecho en el bloque **Blog_noticias** → **Copy SSH Command** → pegar en la terminal local y ejecutar.

```bash
railway login   # abre el navegador para autenticarse
# luego pegar el comando SSH copiado del dashboard
```

### Dentro del contenedor

El venv de producción está en `/opt/venv/`. Usar ese Python:

```bash
/opt/venv/bin/python manage.py createsuperuser
```

---

## 26. Verificación final

Una vez completado el deploy, verificar que todo funcione:

| URL | Qué verificar |
|---|---|
| `https://tu-app.up.railway.app/` | Página de inicio carga con CSS correcto |
| `https://tu-app.up.railway.app/admin/` | Panel admin accesible con el superusuario |
| `https://tu-app.up.railway.app/feed/` | XML del RSS sin errores |
| `https://tu-app.up.railway.app/sitemap.xml` | XML del sitemap sin errores |
| `https://tu-app.up.railway.app/static/css/estilos.css` | 200 OK (no 404) |

También ejecutar localmente (con las variables de entorno seteadas):

```bash
python manage.py check --deploy
```

Warnings esperados y su estado:

| Warning | Estado | Razón |
|---|---|---|
| `SECURE_SSL_REDIRECT` | ✅ Resuelto | Activado cuando `DEBUG=False` |
| `SESSION_COOKIE_SECURE` | ✅ Resuelto | Activado cuando `DEBUG=False` |
| `CSRF_COOKIE_SECURE` | ✅ Resuelto | Activado cuando `DEBUG=False` |
| `SECURE_HSTS_SECONDS` | ⚠️ No bloqueante | Railway maneja HSTS a nivel de plataforma |

---

## 27. Limitación conocida: archivos media

Railway tiene **filesystem efímero** — los archivos subidos (`media/`) se pierden en cada redeploy. Intentar subir imágenes desde el admin genera un error 500.

**Impacto:** las noticias funcionan perfectamente sin imágenes. El texto siempre está en PostgreSQL y persiste entre deploys.

**Solución futura:** migrar `ImageField` a almacenamiento externo con `django-storages`:
- **Cloudflare R2** — gratuito hasta 10 GB, sin costo de egress (recomendado)
- **AWS S3** — el estándar de la industria

La migración requiere instalar `django-storages`, crear un bucket en el servicio elegido y configurar unas pocas variables de entorno adicionales.

---

## 28. Comandos de referencia rápida

```bash
# ── Entorno local ──────────────────────────────────────────

# Activar entorno virtual
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# Instalar dependencias
pip install -r requirements.txt

# Crear migraciones después de cambiar un modelo
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Verificar configuración
python manage.py check

# Verificar configuración de producción
python manage.py check --deploy

# Crear superusuario
python manage.py createsuperuser

# Iniciar el servidor de desarrollo
python manage.py runserver

# Recolectar archivos estáticos (simular producción)
python manage.py collectstatic

# Shell interactivo de Django
python manage.py shell

# ── Railway CLI ────────────────────────────────────────────

# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Ejecutar comando en el entorno de producción
railway run python manage.py <comando>
```

### Queries útiles en el shell de Django

```python
from noticias.models import Noticia, Categoria

Noticia.objects.all()                                   # todas las noticias
Noticia.objects.filter(categoria__nombre='Economía')    # filtrar por categoría
Noticia.objects.filter(titulo__icontains='dólar')       # buscar en el título
Noticia.objects.count()                                 # contar noticias
Noticia.objects.first()                                 # la más reciente
```

---

*Proyecto construido con Django 5.2 · Bootstrap 5.3 · python-slugify · Pillow · WhiteNoise · gunicorn · PostgreSQL · Railway*
