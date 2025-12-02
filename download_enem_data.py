"""
Script para baixar e processar provas do ENEM em formato JSON/JSONL

Fontes disponíveis:
1. Google Drive (pasta com 21 arquivos JSONL - 2012-2023)
2. API ENEM (enem.dev) - mais de 2.700 questões
3. Microdados INEP (dados oficiais)
"""

import os
import json
import glob
from pathlib import Path
from typing import List, Dict, Optional
import requests


class ENEMDataDownloader:
    """Classe para baixar e processar dados do ENEM."""
    
    # ID da pasta do Google Drive (do notebook)
    GOOGLE_DRIVE_FOLDER_ID = "1datullhe8eo6Ogi5zVV04TJyRl314eDZ"
    
    # API ENEM
    API_ENEM_BASE_URL = "https://api.enem.dev"
    
    def __init__(self, data_dir: str = "provas"):
        """
        Inicializa o downloader.
        
        Args:
            data_dir: Diretório onde os dados serão salvos
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def download_from_google_drive(self) -> bool:
        """
        Baixa o dataset do ENEM do Google Drive usando gdown.
        
        Returns:
            True se download bem-sucedido
        """
        try:
            import subprocess
            
            print("⬇️  Baixando dataset do ENEM do Google Drive...")
            print(f"   Pasta ID: {self.GOOGLE_DRIVE_FOLDER_ID}")
            
            # Verificar se gdown está instalado
            try:
                import gdown
            except ImportError:
                print("   Instalando gdown...")
                subprocess.run(["pip", "install", "-q", "gdown"], check=True)
                import gdown
            
            # Baixar pasta
            url = f"https://drive.google.com/drive/folders/{self.GOOGLE_DRIVE_FOLDER_ID}"
            gdown.download_folder(url, output=str(self.data_dir), quiet=False)
            
            # Verificar arquivos baixados
            arquivos = list(self.data_dir.glob("*.jsonl"))
            if arquivos:
                print(f"✅ Download concluído! {len(arquivos)} arquivos encontrados.")
                for arquivo in arquivos[:5]:  # Mostrar primeiros 5
                    print(f"   - {arquivo.name}")
                if len(arquivos) > 5:
                    print(f"   ... e mais {len(arquivos) - 5} arquivos")
                return True
            else:
                print("⚠️  Nenhum arquivo .jsonl encontrado após download")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao baixar do Google Drive: {e}")
            print("\n💡 Alternativas:")
            print("   1. Baixe manualmente do Google Drive")
            print("   2. Use a API ENEM (enem.dev)")
            print("   3. Use os microdados do INEP")
            return False
    
    def load_jsonl_files(self) -> List[Dict]:
        """
        Carrega todos os arquivos JSONL do diretório.
        
        Returns:
            Lista de questões do ENEM
        """
        arquivos = list(self.data_dir.glob("*.jsonl"))
        
        if not arquivos:
            print(f"❌ Nenhum arquivo .jsonl encontrado em {self.data_dir}")
            return []
        
        print(f"📚 Carregando {len(arquivos)} arquivos .jsonl...")
        
        todas_questoes = []
        
        for arquivo in arquivos:
            try:
                with open(arquivo, 'r', encoding='utf-8') as f:
                    for linha in f:
                        linha = linha.strip()
                        if linha:
                            try:
                                questao = json.loads(linha)
                                todas_questoes.append(questao)
                            except json.JSONDecodeError as e:
                                print(f"   ⚠️  Erro ao parsear linha em {arquivo.name}: {e}")
                                continue
                
                print(f"   ✅ {arquivo.name}: {len([q for q in todas_questoes if q])} questões")
                
            except Exception as e:
                print(f"   ❌ Erro ao ler {arquivo.name}: {e}")
        
        print(f"\n🏆 Total de questões carregadas: {len(todas_questoes)}")
        return todas_questoes
    
    def fetch_from_api_enem(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Busca questões da API ENEM (enem.dev).
        
        Args:
            limit: Número máximo de questões (None = todas)
        
        Returns:
            Lista de questões
        """
        print(f"🌐 Buscando questões da API ENEM (enem.dev)...")
        
        try:
            # API ENEM - endpoint de questões
            url = f"{self.API_ENEM_BASE_URL}/questions"
            
            params = {}
            if limit:
                params['limit'] = limit
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            dados = response.json()
            questoes = dados.get('data', [])
            
            print(f"✅ {len(questoes)} questões obtidas da API")
            return questoes
            
        except Exception as e:
            print(f"❌ Erro ao buscar da API: {e}")
            print("\n💡 Verifique:")
            print("   - Conexão com internet")
            print("   - API enem.dev está online")
            print("   - URL: https://api.enem.dev")
            return []
    
    def save_to_json(self, questoes: List[Dict], filename: str = "enem_questoes.json"):
        """
        Salva questões em arquivo JSON.
        
        Args:
            questoes: Lista de questões
            filename: Nome do arquivo de saída
        """
        output_path = self.data_dir / filename
        
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(questoes, f, ensure_ascii=False, indent=2)
            
            tamanho_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"✅ Questões salvas em: {output_path}")
            print(f"   Total: {len(questoes)} questões")
            print(f"   Tamanho: {tamanho_mb:.2f} MB")
            
        except Exception as e:
            print(f"❌ Erro ao salvar: {e}")
    
    def get_statistics(self, questoes: List[Dict]) -> Dict:
        """
        Gera estatísticas sobre as questões.
        
        Args:
            questoes: Lista de questões
        
        Returns:
            Dicionário com estatísticas
        """
        if not questoes:
            return {}
        
        stats = {
            "total": len(questoes),
            "por_ano": {},
            "por_area": {},
            "campos_presentes": set()
        }
        
        for questao in questoes:
            # Por ano
            ano = questao.get('ano') or questao.get('year') or 'desconhecido'
            stats["por_ano"][ano] = stats["por_ano"].get(ano, 0) + 1
            
            # Por área
            area = questao.get('area') or questao.get('subject') or 'desconhecida'
            stats["por_area"][area] = stats["por_area"].get(area, 0) + 1
            
            # Campos presentes
            stats["campos_presentes"].update(questao.keys())
        
        stats["campos_presentes"] = sorted(list(stats["campos_presentes"]))
        
        return stats


def main():
    """Função principal."""
    print("=" * 80)
    print("📥 DOWNLOAD E PROCESSAMENTO DE DADOS DO ENEM")
    print("=" * 80)
    print()
    
    downloader = ENEMDataDownloader()
    
    # Opção 1: Baixar do Google Drive
    print("Opção 1: Baixar do Google Drive")
    print("-" * 80)
    if downloader.download_from_google_drive():
        questoes = downloader.load_jsonl_files()
        if questoes:
            stats = downloader.get_statistics(questoes)
            print("\n📊 Estatísticas:")
            print(f"   Total de questões: {stats.get('total', 0)}")
            print(f"   Anos disponíveis: {len(stats.get('por_ano', {}))}")
            print(f"   Áreas: {', '.join(stats.get('por_area', {}).keys())}")
            
            # Salvar em JSON único
            downloader.save_to_json(questoes, "enem_questoes_completo.json")
    
    print("\n" + "=" * 80)
    print("Opção 2: Buscar da API ENEM (enem.dev)")
    print("-" * 80)
    
    # Opção 2: API ENEM
    questoes_api = downloader.fetch_from_api_enem(limit=100)  # Limitar para teste
    if questoes_api:
        downloader.save_to_json(questoes_api, "enem_questoes_api.json")
    
    print("\n" + "=" * 80)
    print("✅ PROCESSO CONCLUÍDO")
    print("=" * 80)
    print("\n💡 Próximos passos:")
    print("   1. Verifique os arquivos em: enem_dados/")
    print("   2. Use os dados para treinar ou testar o modelo")
    print("   3. Consulte a documentação da API: https://enem.dev")


if __name__ == "__main__":
    main()

