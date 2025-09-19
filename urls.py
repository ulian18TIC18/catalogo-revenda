from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from produtos.views import ProdutoViewSet  # Import do app produtos

# Configurando o router da API
router = routers.DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename='produto')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  # Inclui todas as rotas do router
]
