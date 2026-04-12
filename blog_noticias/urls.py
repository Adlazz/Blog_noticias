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
