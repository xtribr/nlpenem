"""
Demonstração: 5 questões aleatórias do ENEM

Mostra questões e prepara para resolução quando API key estiver configurada.
"""

import json
import random
from typing import List, Dict


def get_questoes_exemplo() -> List[Dict]:
    """Retorna 5 questões de exemplo do ENEM."""
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
            "gabarito": "D",
            "explicacao": "Custo total = 5 + 2x, onde x é a distância. 21 = 5 + 2x, então 2x = 16, x = 8 km"
        },
        {
            "ano": 2022,
            "area": "Ciências Humanas",
            "questao": "A Teoria da Resposta ao Item (TRI) utilizada no ENEM permite:",
            "alternativas": {
                "A": "Comparar provas de diferentes edições do exame",
                "B": "Usar apenas a nota bruta dos candidatos",
                "C": "Ignorar o nível de dificuldade dos itens",
                "D": "Eliminar a necessidade de gabarito oficial",
                "E": "Calcular apenas médias aritméticas simples"
            },
            "gabarito": "A",
            "explicacao": "A TRI permite comparar desempenhos entre diferentes edições do ENEM, considerando a dificuldade dos itens."
        },
        {
            "ano": 2023,
            "area": "Linguagens e Códigos",
            "questao": "No ENEM, a área de Linguagens e Códigos avalia principalmente:",
            "alternativas": {
                "A": "Apenas regras gramaticais",
                "B": "Apenas obras literárias",
                "C": "Leitura, interpretação e produção textual",
                "D": "Apenas a redação",
                "E": "Apenas língua estrangeira"
            },
            "gabarito": "C",
            "explicacao": "A área de Linguagens e Códigos avalia habilidades de leitura, interpretação e produção textual em português e língua estrangeira."
        },
        {
            "ano": 2022,
            "area": "Ciências da Natureza",
            "questao": "A nota TRI no ENEM varia de:",
            "alternativas": {
                "A": "0 a 100 pontos",
                "B": "0 a 500 pontos",
                "C": "200 a 800 pontos",
                "D": "300 a 1000 pontos",
                "E": "0 a 1000 pontos"
            },
            "gabarito": "E",
            "explicacao": "A nota TRI no ENEM varia de 0 a 1000 pontos para cada área de conhecimento."
        },
        {
            "ano": 2023,
            "area": "Matemática",
            "questao": "Um estudante obteve notas 650, 700, 680 e 720 nas quatro áreas do ENEM (CH, CN, LC, MT). Qual é a média aritmética dessas notas?",
            "alternativas": {
                "A": "675,00",
                "B": "680,00",
                "C": "687,50",
                "D": "690,00",
                "E": "695,00"
            },
            "gabarito": "C",
            "explicacao": "Média = (650 + 700 + 680 + 720) / 4 = 2750 / 4 = 687,50"
        }
    ]


def mostrar_questoes(questoes: List[Dict], resolver: bool = False):
    """Mostra as questões e opcionalmente resolve com o modelo."""
    
    print("=" * 80)
    print("🎓 QUESTÕES DO ENEM")
    print("=" * 80)
    print()
    
    # Tentar resolver se solicitado
    client = None
    if resolver:
        try:
            # Garantir que .env seja carregado antes
            import os
            from pathlib import Path
            
            env_path = Path(__file__).parent / '.env'
            if env_path.exists():
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            if key.strip() == 'MARITACA_API_KEY':
                                api_key = value.strip()
                                # Remover aspas se houver
                                if api_key.startswith('"') and api_key.endswith('"'):
                                    api_key = api_key[1:-1]
                                if api_key.startswith("'") and api_key.endswith("'"):
                                    api_key = api_key[1:-1]
                                os.environ['MARITACA_API_KEY'] = api_key.strip()
                                break
            
            # Agora importar e usar
            from maritaca_api import MaritacaAPI
            client = MaritacaAPI()  # Vai usar a env var que acabamos de definir
            print("✅ Modelo conectado - Resolvendo questões...\n")
        except ValueError as e:
            print(f"⚠️  {e}\n")
            print("Mostrando apenas as questões...\n")
            print("💡 Configure a API key no arquivo .env\n")
        except Exception as e:
            print(f"⚠️  Erro ao conectar modelo: {e}\n")
            import traceback
            traceback.print_exc()
            print("\nMostrando apenas as questões...\n")
    
    resultados = []
    
    for i, questao in enumerate(questoes, 1):
        print("=" * 80)
        print(f"QUESTÃO {i}/{len(questoes)} - {questao['area']} ({questao['ano']})")
        print("=" * 80)
        print()
        print(f"📝 {questao['questao']}")
        print()
        print("Alternativas:")
        for letra, texto in questao['alternativas'].items():
            print(f"   {letra}) {texto}")
        print()
        
        if questao.get('gabarito'):
            print(f"✅ Gabarito oficial: {questao['gabarito']}")
        
        if questao.get('explicacao'):
            print(f"💡 Explicação: {questao['explicacao']}")
        
        # Tentar resolver com modelo
        if client:
            print("\n🤖 Resposta do modelo:")
            print("-" * 80)
            
            prompt = f"""Questão do ENEM {questao['ano']} - {questao['area']}

{questao['questao']}

"""
            for letra, texto in questao['alternativas'].items():
                prompt += f"{letra}) {texto}\n"
            
            prompt += "\nResolva esta questão passo a passo e indique a alternativa correta:"
            
            try:
                resposta = client.generate_enem_response(
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=400
                )
                print(resposta)
                
                # Verificar acerto
                resposta_upper = resposta.upper()
                gabarito_upper = str(questao['gabarito']).upper()
                acertou = gabarito_upper in resposta_upper or f"ALTERNATIVA {gabarito_upper}" in resposta_upper
                
                status = "✅ CORRETO" if acertou else "❌ INCORRETO"
                print(f"\n{status}")
                
                resultados.append({
                    "questao": i,
                    "gabarito": questao['gabarito'],
                    "acertou": acertou
                })
                
            except Exception as e:
                print(f"❌ Erro: {e}")
                resultados.append({
                    "questao": i,
                    "erro": str(e)
                })
        
        print("\n")
    
    # Resumo se resolveu
    if client and resultados:
        print("=" * 80)
        print("📊 RESUMO")
        print("=" * 80)
        print()
        
        acertos = sum(1 for r in resultados if r.get('acertou') == True)
        erros = sum(1 for r in resultados if r.get('acertou') == False)
        total = len(resultados)
        
        print(f"Total de questões resolvidas: {total}")
        print(f"✅ Acertos: {acertos}")
        print(f"❌ Erros: {erros}")
        if acertos + erros > 0:
            taxa = (acertos / (acertos + erros)) * 100
            print(f"📈 Taxa de acerto: {taxa:.2f}%")
        print()


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Mostra e resolve questões do ENEM')
    parser.add_argument(
        '-r', '--resolver',
        action='store_true',
        help='Tentar resolver as questões com o modelo (requer MARITACA_API_KEY)'
    )
    parser.add_argument(
        '-n', '--num',
        type=int,
        default=5,
        help='Número de questões (padrão: 5)'
    )
    
    args = parser.parse_args()
    
    # Obter questões
    todas_questoes = get_questoes_exemplo()
    questoes = random.sample(todas_questoes, min(args.num, len(todas_questoes)))
    
    # Mostrar e resolver
    mostrar_questoes(questoes, resolver=args.resolver)


if __name__ == "__main__":
    main()

