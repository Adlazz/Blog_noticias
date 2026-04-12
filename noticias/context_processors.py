from .models import Categoria


def categorias_globales(request):
    return {'categorias_nav': Categoria.objects.all()}
