from django.contrib import admin

# Register your models here.

from produtos.models import Produto

@admin.register(Produto)
class ProdutoAdmim(admin.ModelAdmin):
    list_display = ("nome", "descricao", "preco", "imagem")
    search_fields = ("nome", )
