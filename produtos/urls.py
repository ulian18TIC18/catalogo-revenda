from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from produtos.views import ProdutoViewSet

router = routers.DefaultRouter()
router.register(r'produtos', ProdutoViewSet) 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),  
]
