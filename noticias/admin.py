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
