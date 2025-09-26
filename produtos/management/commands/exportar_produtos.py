import os
import json
import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from produtos.models import Produto
import hashlib

def calcular_hash(arquivo):
    """Retorna o hash md5 do arquivo para comparar alterações"""
    hash_md5 = hashlib.md5()
    with open(arquivo, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

class Command(BaseCommand):
    help = "Exporta os produtos para produtos.json e copia as imagens atualizadas para o frontend"

    def handle(self, *args, **kwargs):
        # Caminho direto para a pasta do frontend
        frontend_path = os.path.join(settings.BASE_DIR, "cosmeticos-frontend")
        json_path = os.path.join(frontend_path, "produtos.json")
        
        # Aponta diretamente para a pasta de imagens existente no frontend
        imagens_destino = os.path.join(frontend_path, "imagens_produtos")
        os.makedirs(imagens_destino, exist_ok=True)

        produtos_data = []
        imagens_atualizadas = 0

        for produto in Produto.objects.all():
            imagem_nome = None

            if produto.imagem:
                # Apenas o nome do arquivo, sem diretórios adicionais
                imagem_nome = os.path.basename(produto.imagem.name)

                # Caminho completo da imagem no MEDIA_ROOT
                imagem_origem = os.path.join(settings.MEDIA_ROOT, produto.imagem.name)

                # Caminho final no frontend (sempre direto em imagens_destino)
                imagem_destino = os.path.join(imagens_destino, imagem_nome)

                try:
                    # Copia apenas se não existir ou estiver diferente
                    if not os.path.exists(imagem_destino) or \
                       calcular_hash(imagem_origem) != calcular_hash(imagem_destino):
                        shutil.copy(imagem_origem, imagem_destino)
                        imagens_atualizadas += 1
                except FileNotFoundError:
                    self.stdout.write(self.style.WARNING(f"Imagem não encontrada: {imagem_origem}"))

            produtos_data.append({
                "id": produto.id,
                "nome": produto.nome,
                "descricao": produto.descricao,
                "preco": float(produto.preco),
                "imagem": f"imagens_produtos/{imagem_nome}" if imagem_nome else None
            })

        # Exporta JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(produtos_data, f, ensure_ascii=False, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"Exportação concluída: {json_path}\n"
            f"Total de produtos exportados: {len(produtos_data)}\n"
            f"Imagens atualizadas: {imagens_atualizadas}"
        ))
