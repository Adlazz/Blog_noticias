from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Noticia, Categoria


class HomeView(ListView):
    model = Noticia
    template_name = 'home.html'
    context_object_name = 'noticias'

    def get_queryset(self):
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
    paginate_by = 10

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
    template_name = 'lista_noticias.html'
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
            return Noticia.objects.filter(
                Q(titulo__icontains=q) | Q(cuerpo__icontains=q)
            )
        return Noticia.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


home = HomeView.as_view()
lista_noticias = ListaNoticiasView.as_view()
detalle_noticia = DetalleNoticiaView.as_view()
categoria = CategoriaView.as_view()
noticias_por_fecha = NoticiasPorFechaView.as_view()
buscar = BuscadorView.as_view()
