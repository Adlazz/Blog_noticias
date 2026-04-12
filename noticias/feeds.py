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
        return strip_tags(item.cuerpo)[:300]

    def item_pubdate(self, item):
        return item.fecha_publicacion

    def item_author_name(self, item):
        return item.autor.get_full_name() or item.autor.username
