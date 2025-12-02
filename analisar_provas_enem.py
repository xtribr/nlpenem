"""
Análise completa dos 21 arquivos de provas do ENEM
"""

import json
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List
import statistics

def analisar_provas_enem(pasta_provas: str = "provas"):
    """Analisa todos os arquivos JSONL das provas do ENEM."""
    
    pasta = Path(pasta_provas)
    
    if not pasta.exists():
        print(f"❌ Pasta '{pasta_provas}' não encontrada!")
        return
    
    arquivos = sorted(list(pasta.glob("*.jsonl")))
    
    if not arquivos:
        print(f"❌ Nenhum arquivo .jsonl encontrado em '{pasta_provas}'")
        return
    
    print("=" * 80)
    print("📊 ANÁLISE COMPLETA DAS PROVAS DO ENEM")
    print("=" * 80)
    print()
    print(f"📁 Pasta: {pasta.absolute()}")
    print(f"📄 Total de arquivos: {len(arquivos)}")
    print()
    
    # Estatísticas gerais
    todas_questoes = []
    stats_por_arquivo = []
    areas_counter = Counter()
    anos_counter = Counter()
    temas_counter = Counter()
    dificuldades_counter = Counter()
    
    # Campos presentes
    campos_todos = set()
    
    # Análise por arquivo
    print("=" * 80)
    print("📋 ANÁLISE POR ARQUIVO")
    print("=" * 80)
    print()
    
    for arquivo in arquivos:
        questoes_arquivo = []
        areas_arquivo = Counter()
        anos_arquivo = Counter()
        
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha_num, linha in enumerate(f, 1):
                    linha = linha.strip()
                    if linha:
                        try:
                            questao = json.loads(linha)
                            questoes_arquivo.append(questao)
                            
                            # Coletar estatísticas
                            ano = questao.get('ano') or questao.get('year') or questao.get('edicao', 'N/A')
                            area = questao.get('area') or questao.get('subject') or questao.get('disciplina', 'N/A')
                            tema = questao.get('tema') or questao.get('topic') or questao.get('assunto', 'N/A')
                            dificuldade = questao.get('dificuldade') or questao.get('difficulty', 'N/A')
                            
                            anos_arquivo[ano] += 1
                            areas_arquivo[area] += 1
                            areas_counter[area] += 1
                            anos_counter[ano] += 1
                            temas_counter[tema] += 1
                            dificuldades_counter[dificuldade] += 1
                            
                            # Campos presentes
                            campos_todos.update(questao.keys())
                            
                        except json.JSONDecodeError as e:
                            print(f"   ⚠️  Erro na linha {linha_num} de {arquivo.name}: {e}")
                            continue
            
            todas_questoes.extend(questoes_arquivo)
            
            # Tamanho do arquivo
            tamanho_mb = arquivo.stat().st_size / (1024 * 1024)
            
            stats_arquivo = {
                "arquivo": arquivo.name,
                "questoes": len(questoes_arquivo),
                "tamanho_mb": tamanho_mb,
                "anos": dict(anos_arquivo),
                "areas": dict(areas_arquivo)
            }
            stats_por_arquivo.append(stats_arquivo)
            
            # Mostrar resumo do arquivo
            print(f"📄 {arquivo.name}")
            print(f"   Questões: {len(questoes_arquivo)}")
            print(f"   Tamanho: {tamanho_mb:.2f} MB")
            if anos_arquivo:
                print(f"   Anos: {', '.join(map(str, sorted(anos_arquivo.keys())))}")
            if areas_arquivo:
                print(f"   Áreas: {', '.join(areas_arquivo.keys())}")
            print()
            
        except Exception as e:
            print(f"❌ Erro ao processar {arquivo.name}: {e}")
            print()
    
    # Estatísticas gerais
    print("=" * 80)
    print("📊 ESTATÍSTICAS GERAIS")
    print("=" * 80)
    print()
    
    print(f"✅ Total de questões: {len(todas_questoes):,}")
    print()
    
    # Por ano
    print("📅 Distribuição por Ano:")
    for ano, count in sorted(anos_counter.items()):
        print(f"   {ano}: {count:,} questões")
    print()
    
    # Por área
    print("📚 Distribuição por Área:")
    for area, count in sorted(areas_counter.items(), key=lambda x: x[1], reverse=True):
        porcentagem = (count / len(todas_questoes)) * 100
        print(f"   {area}: {count:,} questões ({porcentagem:.2f}%)")
    print()
    
    # Por dificuldade
    if dificuldades_counter:
        print("🎯 Distribuição por Dificuldade:")
        for dificuldade, count in sorted(dificuldades_counter.items(), key=lambda x: x[1], reverse=True):
            porcentagem = (count / len(todas_questoes)) * 100
            print(f"   {dificuldade}: {count:,} questões ({porcentagem:.2f}%)")
        print()
    
    # Top temas
    if temas_counter:
        print("🏷️  Top 10 Temas:")
        for tema, count in temas_counter.most_common(10):
            print(f"   {tema}: {count:,} questões")
        print()
    
    # Estatísticas de tamanho
    questoes_por_arquivo = [s['questoes'] for s in stats_por_arquivo]
    if questoes_por_arquivo:
        print("📈 Estatísticas de Questões por Arquivo:")
        print(f"   Média: {statistics.mean(questoes_por_arquivo):.2f}")
        print(f"   Mediana: {statistics.median(questoes_por_arquivo):.2f}")
        print(f"   Mínimo: {min(questoes_por_arquivo)}")
        print(f"   Máximo: {max(questoes_por_arquivo)}")
        print()
    
    # Campos presentes
    print("🔍 Campos Presentes nos Dados:")
    campos_ordenados = sorted(campos_todos)
    for campo in campos_ordenados:
        print(f"   - {campo}")
    print()
    
    # Resumo por arquivo (tabela)
    print("=" * 80)
    print("📋 RESUMO TABULAR POR ARQUIVO")
    print("=" * 80)
    print()
    print(f"{'Arquivo':<40} {'Questões':<12} {'Tamanho (MB)':<15}")
    print("-" * 80)
    for stats in sorted(stats_por_arquivo, key=lambda x: x['arquivo']):
        print(f"{stats['arquivo']:<40} {stats['questoes']:<12,} {stats['tamanho_mb']:<15.2f}")
    print()
    
    # Salvar estatísticas em JSON
    output_file = Path("estatisticas_provas_enem.json")
    estatisticas_completas = {
        "total_questoes": len(todas_questoes),
        "total_arquivos": len(arquivos),
        "por_ano": dict(anos_counter),
        "por_area": dict(areas_counter),
        "por_dificuldade": dict(dificuldades_counter),
        "top_temas": dict(temas_counter.most_common(20)),
        "campos_presentes": sorted(list(campos_todos)),
        "estatisticas_por_arquivo": stats_por_arquivo,
        "estatisticas_gerais": {
            "media_questoes_por_arquivo": statistics.mean(questoes_por_arquivo) if questoes_por_arquivo else 0,
            "mediana_questoes_por_arquivo": statistics.median(questoes_por_arquivo) if questoes_por_arquivo else 0,
            "min_questoes": min(questoes_por_arquivo) if questoes_por_arquivo else 0,
            "max_questoes": max(questoes_por_arquivo) if questoes_por_arquivo else 0
        }
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(estatisticas_completas, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Estatísticas salvas em: {output_file}")
    print()
    print("=" * 80)
    print("✅ ANÁLISE CONCLUÍDA")
    print("=" * 80)


if __name__ == "__main__":
    analisar_provas_enem("provas")


