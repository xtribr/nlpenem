"""
Script para resolver questões aleatórias do ENEM usando o modelo fine-tuned

Busca questões da API ENEM ou arquivos locais e pede para o modelo resolver.
"""

import os
import sys
import json
import random
from pathlib import Path
from typing import List, Dict, Optional

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from maritaca_api import MaritacaAPI
    USE_API = True
except ImportError:
    print("❌ maritaca_api.py não encontrado. Instale: pip install requests")
    sys.exit(1)


def buscar_questoes_exemplo() -> List[Dict]:
    """
    Retorna questões de exemplo para teste.
    
    Returns:
        Lista de questões de exemplo
    """
    return [
        {
            "ano": 2023,
            "area": "Matemática",
            "questao": "Uma empresa de delivery cobra R$ 5,00 pela entrega mais R$ 2,00 por quilômetro rodado. Se um cliente pagou R$ 21,00, quantos quilômetros foram percorridos?",
            "alternativas": {
                "A": "5 km",
                "B": "6 km",
                "C": "7 km",
                "D": "8 km",
                "E": "9 km"
            },
            "gabarito": "D"
        },
        {
            "ano": 2022,
            "area": "Ciências Humanas",
            "questao": "A Teoria da Resposta ao Item (TRI) utilizada no ENEM permite:",
            "alternativas": {
                "A": "Comparar provas de diferentes edições",
                "B": "Usar apenas nota bruta",
                "C": "Ignorar o nível de dificuldade",
                "D": "Eliminar a necessidade de gabarito",
                "E": "Calcular apenas médias simples"
            },
            "gabarito": "A"
        },
        {
            "ano": 2023,
            "area": "Linguagens e Códigos",
            "questao": "No ENEM, a área de Linguagens e Códigos avalia principalmente:",
            "alternativas": {
                "A": "Apenas gramática",
                "B": "Apenas literatura",
                "C": "Leitura, interpretação e produção textual",
                "D": "Apenas redação",
                "E": "Apenas língua estrangeira"
            },
            "gabarito": "C"
        },
        {
            "ano": 2022,
            "area": "Ciências da Natureza",
            "questao": "A nota TRI no ENEM varia de:",
            "alternativas": {
                "A": "0 a 100",
                "B": "0 a 500",
                "C": "200 a 800",
                "D": "300 a 1000",
                "E": "0 a 1000"
            },
            "gabarito": "E"
        },
        {
            "ano": 2023,
            "area": "Matemática",
            "questao": "Um estudante obteve notas 650, 700, 680 e 720 nas quatro áreas do ENEM. Qual é a média aritmética dessas notas?",
            "alternativas": {
                "A": "675",
                "B": "680",
                "C": "687.50",
                "D": "690",
                "E": "695"
            },
            "gabarito": "C"
        }
    ]


def buscar_questoes_api(num_questoes: int = 5) -> List[Dict]:
    """
    Busca questões aleatórias da API ENEM.
    
    Args:
        num_questoes: Número de questões a buscar
    
    Returns:
        Lista de questões
    """
    import requests
    
    print(f"🌐 Buscando {num_questoes} questões da API ENEM...")
    
    try:
        # Buscar questões da API
        url = "https://api.enem.dev/questions"
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        dados = response.json()
        todas_questoes = dados.get('data', [])
        
        if not todas_questoes:
            print("⚠️  Nenhuma questão retornada da API")
            return []
        
        # Selecionar aleatórias
        questoes_selecionadas = random.sample(
            todas_questoes, 
            min(num_questoes, len(todas_questoes))
        )
        
        print(f"✅ {len(questoes_selecionadas)} questões selecionadas")
        return questoes_selecionadas
        
    except Exception as e:
        print(f"❌ Erro ao buscar da API: {e}")
        return []


def buscar_questoes_locais(num_questoes: int = 5) -> List[Dict]:
    """
    Busca questões de arquivos JSONL locais.
    
    Args:
        num_questoes: Número de questões a buscar
    
    Returns:
        Lista de questões
    """
    data_dir = Path("provas")
    
    if not data_dir.exists():
        print(f"⚠️  Diretório {data_dir} não encontrado")
        return []
    
    arquivos_jsonl = list(data_dir.glob("*.jsonl"))
    
    if not arquivos_jsonl:
        print(f"⚠️  Nenhum arquivo .jsonl encontrado em {data_dir}")
        return []
    
    print(f"📚 Carregando questões de {len(arquivos_jsonl)} arquivos...")
    
    todas_questoes = []
    
    for arquivo in arquivos_jsonl:
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                for linha in f:
                    linha = linha.strip()
                    if linha:
                        try:
                            questao = json.loads(linha)
                            todas_questoes.append(questao)
                        except json.JSONDecodeError:
                            continue
        except Exception as e:
            print(f"   ⚠️  Erro ao ler {arquivo.name}: {e}")
    
    if not todas_questoes:
        print("❌ Nenhuma questão encontrada nos arquivos locais")
        return []
    
    # Selecionar aleatórias
    questoes_selecionadas = random.sample(
        todas_questoes,
        min(num_questoes, len(todas_questoes))
    )
    
    print(f"✅ {len(questoes_selecionadas)} questões selecionadas de {len(todas_questoes)} disponíveis")
    return questoes_selecionadas


def formatar_questao(questao: Dict) -> str:
    """
    Formata uma questão para o prompt do modelo.
    
    Args:
        questao: Dicionário com dados da questão
    
    Returns:
        String formatada
    """
    # Tentar diferentes formatos de dados
    ano = questao.get('ano') or questao.get('year') or questao.get('edicao', 'N/A')
    area = questao.get('area') or questao.get('subject') or questao.get('disciplina', 'N/A')
    
    texto = questao.get('questao') or questao.get('question') or questao.get('texto', '')
    alternativas = questao.get('alternativas') or questao.get('alternatives') or {}
    gabarito = questao.get('gabarito') or questao.get('correct_answer') or questao.get('resposta', '')
    
    # Formatar prompt
    prompt = f"""Questão do ENEM {ano} - {area}

{texto}

"""
    
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
    
    return prompt, gabarito


def resolver_questoes(num_questoes: int = 5):
    """Resolve questões aleatórias do ENEM."""
    
    print("=" * 80)
    print("🎓 RESOLUÇÃO DE QUESTÕES DO ENEM")
    print("=" * 80)
    print()
    
    # Verificar API key (já carregada do .env pelo maritaca_api)
    api_key = os.getenv("MARITACA_API_KEY")
    if not api_key:
        # Tentar carregar do .env manualmente
        env_path = Path(__file__).parent / '.env'
        if env_path.exists():
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        if key.strip() == 'MARITACA_API_KEY':
                            api_key = value.strip()
                            os.environ['MARITACA_API_KEY'] = value.strip()
                            break
    
    if not api_key:
        print("❌ Erro: MARITACA_API_KEY não encontrada!")
        print("\nConfigure no arquivo .env ou como variável de ambiente:")
        print("  echo 'MARITACA_API_KEY=sua-chave' > .env")
        return
    
    # Inicializar cliente
    try:
        client = MaritacaAPI(api_key=api_key)
        print("✅ Cliente API inicializado\n")
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return
    
    # Buscar questões
    print("📥 Buscando questões...")
    questoes = buscar_questoes_locais(num_questoes)
    
    if not questoes:
        print("\n💡 Tentando buscar da API ENEM...")
        questoes = buscar_questoes_api(num_questoes)
    
    if not questoes:
        print("\n💡 Usando questões de exemplo...")
        questoes_exemplo = buscar_questoes_exemplo()
        questoes = random.sample(questoes_exemplo, min(num_questoes, len(questoes_exemplo)))
        print(f"✅ {len(questoes)} questões de exemplo selecionadas")
    
    print(f"\n✅ {len(questoes)} questões obtidas\n")
    
    # Resolver cada questão
    resultados = []
    
    for i, questao in enumerate(questoes, 1):
        print("=" * 80)
        print(f"QUESTÃO {i}/{len(questoes)}")
        print("=" * 80)
        print()
        
        # Formatar questão
        prompt, gabarito = formatar_questao(questao)
        
        # Mostrar questão
        print("📝 Questão:")
        print("-" * 80)
        print(prompt)
        print("-" * 80)
        
        if gabarito:
            print(f"\n✅ Gabarito oficial: {gabarito}")
        
        print("\n🤖 Resposta do modelo:")
        print("-" * 80)
        
        try:
            # Gerar resposta
            resposta = client.generate_enem_response(
                prompt=prompt,
                temperature=0.7,
                max_tokens=500
            )
            
            print(resposta)
            
            # Verificar se acertou (se tiver gabarito)
            acertou = None
            if gabarito:
                resposta_upper = resposta.upper()
                gabarito_upper = str(gabarito).upper()
                acertou = gabarito_upper in resposta_upper or f"ALTERNATIVA {gabarito_upper}" in resposta_upper
            
            resultados.append({
                "questao_num": i,
                "gabarito": gabarito,
                "resposta_modelo": resposta,
                "acertou": acertou
            })
            
            if acertou is not None:
                status = "✅ CORRETO" if acertou else "❌ INCORRETO"
                print(f"\n{status}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar resposta: {e}")
            resultados.append({
                "questao_num": i,
                "erro": str(e)
            })
        
        print("\n")
    
    # Resumo final
    print("=" * 80)
    print("📊 RESUMO")
    print("=" * 80)
    print()
    
    total = len(resultados)
    acertos = sum(1 for r in resultados if r.get('acertou') == True)
    erros = sum(1 for r in resultados if r.get('acertou') == False)
    sem_gabarito = sum(1 for r in resultados if r.get('acertou') is None)
    
    print(f"Total de questões: {total}")
    if acertos + erros > 0:
        print(f"✅ Acertos: {acertos}")
        print(f"❌ Erros: {erros}")
        taxa = (acertos / (acertos + erros)) * 100 if (acertos + erros) > 0 else 0
        print(f"📈 Taxa de acerto: {taxa:.2f}%")
    if sem_gabarito > 0:
        print(f"⚪ Sem gabarito para comparação: {sem_gabarito}")
    
    print("\n" + "=" * 80)


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Resolve questões aleatórias do ENEM')
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=5,
        help='Número de questões a resolver (padrão: 5)'
    )
    
    args = parser.parse_args()
    
    try:
        resolver_questoes(num_questoes=args.num)
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

