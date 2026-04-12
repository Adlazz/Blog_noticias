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
