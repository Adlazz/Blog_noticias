from django.contrib.sitemaps import Sitemap
from .models import Noticia


class NoticiasSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.8

    def items(self):
        return Noticia.objects.all()

    def lastmod(self, obj):
        return obj.fecha_publicacion
