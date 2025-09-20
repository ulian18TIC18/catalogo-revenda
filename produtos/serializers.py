from rest_framework import serializers
from produtos.models import Produto, Categoria

class ProdutoSerializer(serializers.ModelSerializer):
    categoria = serializers.CharField(source="categoria.nome", read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'nome', 'descricao', 'preco', 'imagem', 'categoria']
