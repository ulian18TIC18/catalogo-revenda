import os
import json
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from produtos.models import Produto


class Command(BaseCommand):
    help = "Exporta os produtos para produtos.json e copia as imagens para o frontend"

    def handle(self, *args, **kwargs):
        # Caminho do frontend 
        frontend_path = os.path.join(settings.BASE_DIR, "cosmeticos-frontend")
        json_path = os.path.join(frontend_path, "produtos.json")
        imagens_destino = os.path.join(frontend_path, "imagens_produtos")

        # Garantir que a pasta de imagens existe
        os.makedirs(imagens_destino, exist_ok=True)

        produtos_data = []

        for produto in Produto.objects.all():
            imagem_nome = None

            if produto.imagem:
                imagem_nome = os.path.basename(produto.imagem.name)

                # Caminho da imagem no MEDIA_ROOT
                imagem_origem = os.path.join(settings.MEDIA_ROOT, produto.imagem.name)

                # Caminho final no frontend
                imagem_destino = os.path.join(imagens_destino, imagem_nome)

                try:
                    shutil.copy(imagem_origem, imagem_destino)
                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(f"Imagem não encontrada: {imagem_origem}"))

            produtos_data.append({
                "id": produto.id,
                "nome": produto.nome,
                "descricao": produto.descricao,
                "preco": float(produto.preco),
                "imagem": f"imagens_produtos/{imagem_nome}" if imagem_nome else None
            })

        # Exportar JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(produtos_data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(f"Exportação concluída: {json_path}"))
