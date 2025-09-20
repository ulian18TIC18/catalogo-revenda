from django.contrib import admin

# Register your models here.

from produtos.models import Produto, Categoria

@admin.register(Produto)
class ProdutoAdmim(admin.ModelAdmin):
    list_display = ("nome", "descricao", "preco", "imagem", "categoria")
    search_fields = ("nome", )

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nome",)
    search_fields = ("nome",)
