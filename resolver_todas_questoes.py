"""
Script para resolver todas as 3.099 questões do ENEM usando o modelo
e gerar relatórios separados por área para treinamento.
"""

import json
import os
import sys
import time
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Dict, Optional
import statistics

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

from maritaca_api import MaritacaAPI

# Mapeamento de áreas
MAPEAMENTO_AREAS = {
    "languages": "LINGUAGENS",
    "human-sciences": "HUMANAS",
    "natural-sciences": "NATUREZA",
    "mathematics": "MATEMATICA",
    "N/A": "OUTRAS"
}

def carregar_todas_questoes(pasta_provas: str = "provas") -> List[Dict]:
    """Carrega todas as questões dos arquivos JSONL."""
    pasta = Path(pasta_provas)
    arquivos = sorted(list(pasta.glob("*.jsonl")))
    
    todas_questoes = []
    
    print(f"📚 Carregando questões de {len(arquivos)} arquivos...")
    
    for arquivo in arquivos:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha_num, linha in enumerate(f, 1):
                    linha = linha.strip()
                    if linha:
                        try:
                            questao = json.loads(linha)
                            # Adicionar nome do arquivo de origem
                            questao['arquivo_origem'] = arquivo.name
                            todas_questoes.append(questao)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"⚠️  Erro ao ler {arquivo.name}: {e}")
    
    print(f"✅ {len(todas_questoes)} questões carregadas\n")
    return todas_questoes


def formatar_questao_para_prompt(questao: Dict) -> tuple:
    """
    Formata questão para prompt do modelo.
    
    Returns:
        (prompt_formatado, gabarito, area)
    """
    # Extrair informações
    texto_questao = questao.get('question') or questao.get('questao') or questao.get('original_question', '')
    contexto = questao.get('context') or questao.get('description', '')
    
    # Alternativas
    alternativas = questao.get('alternatives') or questao.get('alternativas') or questao.get('options', {})
    gabarito = questao.get('answer') or questao.get('gabarito') or questao.get('correct_answer', '')
    
    # Área
    area_raw = questao.get('area') or questao.get('subject') or 'N/A'
    area = MAPEAMENTO_AREAS.get(area_raw, area_raw.upper())
    
    # Montar prompt
    prompt = f"Questão do ENEM - {area}\n\n"
    
    if contexto:
        prompt += f"Contexto: {contexto}\n\n"
    
    prompt += f"{texto_questao}\n\n"
    
    # Adicionar alternativas
    if isinstance(alternativas, dict):
        for letra in ['A', 'B', 'C', 'D', 'E']:
            alt = alternativas.get(letra) or alternativas.get(letra.lower())
            if alt:
                prompt += f"{letra}) {alt}\n"
    elif isinstance(alternativas, list):
        for i, alt in enumerate(alternativas):
            letra = chr(65 + i)  # A, B, C, D, E
            prompt += f"{letra}) {alt}\n"
    
    prompt += "\nResolva esta questão passo a passo e indique a alternativa correta:"
    
    return prompt, str(gabarito).upper().strip(), area


def resolver_questao(client: MaritacaAPI, questao: Dict) -> Dict:
    """Resolve uma questão usando o modelo."""
    prompt, gabarito, area = formatar_questao_para_prompt(questao)
    
    try:
        resposta = client.generate_enem_response(
            prompt=prompt,
            temperature=0.7,
            max_tokens=500
        )
        
        # Verificar se acertou
        resposta_upper = resposta.upper()
        gabarito_upper = gabarito.upper()
        acertou = (
            gabarito_upper in resposta_upper or 
            f"ALTERNATIVA {gabarito_upper}" in resposta_upper or
            f"LETRA {gabarito_upper}" in resposta_upper or
            f"OPÇÃO {gabarito_upper}" in resposta_upper
        )
        
        return {
            "questao_id": questao.get('id') or questao.get('number', ''),
            "arquivo_origem": questao.get('arquivo_origem', ''),
            "area": area,
            "gabarito": gabarito,
            "resposta_modelo": resposta,
            "acertou": acertou,
            "prompt_usado": prompt,
            "questao_original": questao
        }
        
    except Exception as e:
        return {
            "questao_id": questao.get('id') or questao.get('number', ''),
            "arquivo_origem": questao.get('arquivo_origem', ''),
            "area": area,
            "gabarito": gabarito,
            "erro": str(e),
            "questao_original": questao
        }


def processar_todas_questoes(
    questoes: List[Dict],
    salvar_progresso: bool = True,
    intervalo_entre_requisicoes: float = 0.5
) -> List[Dict]:
    """Processa todas as questões com o modelo."""
    
    print("=" * 80)
    print("🤖 RESOLVENDO TODAS AS QUESTÕES COM O MODELO")
    print("=" * 80)
    print()
    
    # Inicializar cliente
    try:
        client = MaritacaAPI()
        print("✅ Cliente API inicializado\n")
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return []
    
    total = len(questoes)
    resultados = []
    arquivo_progresso = Path("progresso_resolucao.json")
    
    # Carregar progresso anterior se existir
    questoes_processadas = set()
    if salvar_progresso and arquivo_progresso.exists():
        try:
            with open(arquivo_progresso, 'r', encoding='utf-8') as f:
                progresso_anterior = json.load(f)
                resultados.extend(progresso_anterior.get('resultados', []))
                questoes_processadas = set(r.get('questao_id', '') for r in resultados)
                print(f"📥 Progresso anterior carregado: {len(resultados)} questões já processadas\n")
        except:
            pass
    
    # Processar questões
    print(f"🔄 Processando {total} questões...")
    print(f"   Intervalo entre requisições: {intervalo_entre_requisicoes}s\n")
    
    for i, questao in enumerate(questoes, 1):
        questao_id = questao.get('id') or questao.get('number', '')
        
        # Pular se já processada
        if questao_id in questoes_processadas:
            continue
        
        print(f"[{i}/{total}] Processando questão {questao_id}...", end=' ', flush=True)
        
        resultado = resolver_questao(client, questao)
        resultados.append(resultado)
        
        if resultado.get('acertou') is not None:
            status = "✅" if resultado['acertou'] else "❌"
            print(f"{status}")
        else:
            print(f"⚠️  Erro")
        
        # Salvar progresso a cada 10 questões
        if salvar_progresso and i % 10 == 0:
            with open(arquivo_progresso, 'w', encoding='utf-8') as f:
                json.dump({
                    "total_processadas": len(resultados),
                    "total_questoes": total,
                    "resultados": resultados
                }, f, ensure_ascii=False, indent=2)
        
        # Intervalo entre requisições
        if i < total:
            time.sleep(intervalo_entre_requisicoes)
    
    print(f"\n✅ Processamento concluído! {len(resultados)} questões processadas\n")
    
    return resultados


def gerar_relatorios_por_area(resultados: List[Dict]):
    """Gera relatórios separados por área."""
    
    print("=" * 80)
    print("📊 GERANDO RELATÓRIOS POR ÁREA")
    print("=" * 80)
    print()
    
    # Separar por área
    resultados_por_area = defaultdict(list)
    
    for resultado in resultados:
        area = resultado.get('area', 'OUTRAS')
        resultados_por_area[area].append(resultado)
    
    # Criar pasta para relatórios
    pasta_relatorios = Path("relatorios_treinamento")
    pasta_relatorios.mkdir(exist_ok=True)
    
    # Estatísticas gerais
    stats_geral = {
        "total_questoes": len(resultados),
        "por_area": {}
    }
    
    # Gerar relatório para cada área
    for area, resultados_area in resultados_por_area.items():
        print(f"📝 Gerando relatório para {area}...")
        
        # Estatísticas da área
        acertos = sum(1 for r in resultados_area if r.get('acertou') == True)
        erros = sum(1 for r in resultados_area if r.get('acertou') == False)
        sem_resposta = sum(1 for r in resultados_area if r.get('acertou') is None)
        total_area = len(resultados_area)
        
        taxa_acerto = (acertos / (acertos + erros)) * 100 if (acertos + erros) > 0 else 0
        
        stats_area = {
            "area": area,
            "total_questoes": total_area,
            "acertos": acertos,
            "erros": erros,
            "sem_resposta": sem_resposta,
            "taxa_acerto": round(taxa_acerto, 2)
        }
        
        stats_geral["por_area"][area] = stats_area
        
        # Salvar relatório JSON da área
        arquivo_relatorio = pasta_relatorios / f"relatorio_{area.lower()}.json"
        with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
            json.dump({
                "estatisticas": stats_area,
                "resultados": resultados_area
            }, f, ensure_ascii=False, indent=2)
        
        # Salvar apenas questões para treinamento (formato simplificado)
        arquivo_treinamento = pasta_relatorios / f"dados_treinamento_{area.lower()}.json"
        dados_treinamento = []
        
        for resultado in resultados_area:
            questao_original = resultado.get('questao_original', {})
            dados_treinamento.append({
                "questao": questao_original.get('question') or questao_original.get('questao', ''),
                "alternativas": questao_original.get('alternatives') or questao_original.get('alternativas', {}),
                "gabarito": resultado.get('gabarito', ''),
                "resposta_modelo": resultado.get('resposta_modelo', ''),
                "acertou": resultado.get('acertou'),
                "area": area
            })
        
        with open(arquivo_treinamento, 'w', encoding='utf-8') as f:
            json.dump(dados_treinamento, f, ensure_ascii=False, indent=2)
        
        print(f"   ✅ {arquivo_relatorio.name} ({total_area} questões)")
        print(f"   ✅ {arquivo_treinamento.name} (dados para treinamento)")
        print(f"   📊 Taxa de acerto: {taxa_acerto:.2f}% ({acertos}/{acertos + erros})")
        print()
    
    # Salvar relatório geral
    arquivo_geral = pasta_relatorios / "relatorio_geral.json"
    with open(arquivo_geral, 'w', encoding='utf-8') as f:
        json.dump(stats_geral, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Relatório geral salvo em: {arquivo_geral}")
    print()
    
    # Gerar relatório em Markdown
    gerar_relatorio_markdown(stats_geral, resultados_por_area, pasta_relatorios)
    
    return stats_geral


def gerar_relatorio_markdown(stats_geral: Dict, resultados_por_area: Dict, pasta: Path):
    """Gera relatório em formato Markdown."""
    
    arquivo_md = pasta / "RELATORIO_TREINAMENTO.md"
    
    with open(arquivo_md, 'w', encoding='utf-8') as f:
        f.write("# 📊 Relatório de Resolução - Questões ENEM\n\n")
        f.write(f"**Data**: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"**Total de Questões**: {stats_geral['total_questoes']:,}\n\n")
        
        f.write("## 📈 Resumo Geral\n\n")
        f.write("| Área | Total | Acertos | Erros | Taxa de Acerto |\n")
        f.write("|------|-------|---------|-------|----------------|\n")
        
        for area, stats in sorted(stats_geral['por_area'].items()):
            f.write(f"| {area} | {stats['total_questoes']} | {stats['acertos']} | {stats['erros']} | {stats['taxa_acerto']:.2f}% |\n")
        
        f.write("\n## 📚 Detalhes por Área\n\n")
        
        for area, resultados_area in sorted(resultados_por_area.items()):
            stats = stats_geral['por_area'][area]
            f.write(f"### {area}\n\n")
            f.write(f"- **Total de Questões**: {stats['total_questoes']}\n")
            f.write(f"- **Acertos**: {stats['acertos']}\n")
            f.write(f"- **Erros**: {stats['erros']}\n")
            f.write(f"- **Taxa de Acerto**: {stats['taxa_acerto']:.2f}%\n\n")
            
            # Top 10 erros mais comuns
            erros_area = [r for r in resultados_area if r.get('acertou') == False]
            if erros_area:
                f.write("#### Questões com Erro (Primeiras 10)\n\n")
                for i, erro in enumerate(erros_area[:10], 1):
                    f.write(f"{i}. Questão {erro.get('questao_id', 'N/A')}\n")
                    f.write(f"   - Gabarito: {erro.get('gabarito', 'N/A')}\n")
                    f.write(f"   - Resposta do modelo: {erro.get('resposta_modelo', '')[:100]}...\n\n")
        
        f.write("\n## 📁 Arquivos Gerados\n\n")
        f.write("- `relatorio_LINGUAGENS.json` - Dados completos de Linguagens\n")
        f.write("- `relatorio_HUMANAS.json` - Dados completos de Humanas\n")
        f.write("- `relatorio_NATUREZA.json` - Dados completos de Natureza\n")
        f.write("- `relatorio_MATEMATICA.json` - Dados completos de Matemática\n")
        f.write("- `dados_treinamento_*.json` - Dados formatados para treinamento\n")
        f.write("- `relatorio_geral.json` - Estatísticas gerais\n")
    
    print(f"✅ Relatório Markdown salvo em: {arquivo_md}")


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Resolve todas as questões do ENEM')
    parser.add_argument(
        '--intervalo',
        type=float,
        default=0.5,
        help='Intervalo entre requisições em segundos (padrão: 0.5)'
    )
    parser.add_argument(
        '--continuar',
        action='store_true',
        help='Continuar processamento anterior'
    )
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("🎓 RESOLUÇÃO COMPLETA DAS QUESTÕES DO ENEM")
    print("=" * 80)
    print()
    
    # Carregar questões
    questoes = carregar_todas_questoes("provas")
    
    if not questoes:
        print("❌ Nenhuma questão encontrada!")
        return
    
    # Processar
    resultados = processar_todas_questoes(
        questoes,
        salvar_progresso=True,
        intervalo_entre_requisicoes=args.intervalo
    )
    
    if not resultados:
        print("❌ Nenhum resultado gerado!")
        return
    
    # Gerar relatórios
    stats = gerar_relatorios_por_area(resultados)
    
    # Resumo final
    print("=" * 80)
    print("✅ PROCESSAMENTO CONCLUÍDO")
    print("=" * 80)
    print()
    print("📊 Resumo Final:")
    for area, stats_area in sorted(stats['por_area'].items()):
        print(f"   {area}: {stats_area['taxa_acerto']:.2f}% de acerto ({stats_area['acertos']}/{stats_area['acertos'] + stats_area['erros']})")
    print()
    print("📁 Relatórios salvos em: relatorios_treinamento/")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Processamento interrompido pelo usuário")
        print("💡 Use --continuar na próxima execução para retomar")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


