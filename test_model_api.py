"""
Script de teste do modelo usando API SABIA-3.1 da Maritaca

Testa o modelo com questões ENEM usando a API ao invés do modelo local.
"""

import os
import sys
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from maritaca_api import MaritacaAPI, test_api_connection
except ImportError as e:
    print(f"❌ Erro ao importar maritaca_api: {e}")
    print("Certifique-se de que o arquivo maritaca_api.py está no mesmo diretório.")
    sys.exit(1)


def test_enem_questions_api():
    """Testa o modelo com questões do ENEM usando a API."""
    print("=" * 80)
    print("🧪 TESTE DO MODELO COM API SABIA-3.1 (MARITACA)")
    print("=" * 80)
    
    # Verificar API key (carregar do .env se necessário)
    api_key = os.getenv("MARITACA_API_KEY")
    if not api_key:
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
                            os.environ['MARITACA_API_KEY'] = value.strip()
                            break
    
    if not api_key:
        print("\n❌ Erro: MARITACA_API_KEY não encontrada!")
        print("\nConfigure no arquivo .env ou como variável de ambiente:")
        print("  echo 'MARITACA_API_KEY=sua-chave' > .env")
        return
    
    print(f"\n✅ API Key encontrada (primeiros 10 chars: {api_key[:10]}...)")
    
    # Testar conexão
    print("\n🔌 Testando conexão com API...")
    if not test_api_connection(api_key):
        print("❌ Falha na conexão com a API")
        return
    
    print("✅ Conexão estabelecida com sucesso!\n")
    
    # Inicializar cliente
    try:
        client = MaritacaAPI(api_key=api_key)
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return
    
    # Casos de teste
    test_cases = [
        {
            "nome": "Questão sobre TRI",
            "prompt": """Questão ENEM: Sobre a Teoria da Resposta ao Item (TRI) utilizada no ENEM, assinale a alternativa correta:

A) A TRI não considera o nível de dificuldade dos itens
B) A TRI permite comparar provas de diferentes edições do exame
C) A TRI utiliza apenas a nota bruta do candidato
D) A TRI não considera o padrão de respostas do candidato
E) A TRI é baseada apenas em estatísticas descritivas simples

Resposta e explicação:""",
            "max_tokens": 300,
            "temperature": 0.7
        },
        {
            "nome": "Explicação de Nota TRI",
            "prompt": "Explique de forma didática o que é a nota TRI no ENEM e como ela difere da nota bruta:",
            "max_tokens": 400,
            "temperature": 0.7
        },
        {
            "nome": "Análise de Desempenho",
            "prompt": """Um estudante obteve as seguintes notas no ENEM:
- Ciências Humanas: 650.00
- Ciências da Natureza: 620.00
- Linguagens e Códigos: 680.00
- Matemática: 700.00
- Redação: 900.00

Analise o desempenho deste estudante e forneça orientações:""",
            "max_tokens": 500,
            "temperature": 0.7
        },
        {
            "nome": "Conceito de Média Ponderada",
            "prompt": "Como é calculada a média do ENEM para ingresso em universidades? Explique o sistema de pesos.",
            "max_tokens": 350,
            "temperature": 0.7
        },
        {
            "nome": "Questão sobre Áreas de Conhecimento",
            "prompt": """Quais são as cinco áreas de conhecimento avaliadas no ENEM e qual a importância de cada uma para a nota final?""",
            "max_tokens": 400,
            "temperature": 0.7
        }
    ]
    
    results = []
    
    print("=" * 80)
    print("📝 EXECUTANDO TESTES COM QUESTÕES ENEM")
    print("=" * 80)
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─' * 80}")
        print(f"Teste {i}/{len(test_cases)}: {test['nome']}")
        print(f"{'─' * 80}\n")
        print(f"Prompt: {test['prompt'][:150]}...\n")
        print("Resposta da API:")
        print("─" * 80)
        
        try:
            response = client.generate_enem_response(
                prompt=test['prompt'],
                temperature=test['temperature'],
                max_tokens=test['max_tokens']
            )
            
            print(response)
            print("\n")
            
            results.append({
                "teste": test['nome'],
                "status": "✅ Sucesso",
                "resposta": response[:200] + "..." if len(response) > 200 else response,
                "tamanho_resposta": len(response)
            })
            
        except Exception as e:
            print(f"❌ Erro: {e}\n")
            results.append({
                "teste": test['nome'],
                "status": f"❌ Erro: {str(e)[:50]}",
                "resposta": None,
                "tamanho_resposta": 0
            })
    
    # Resumo
    print("=" * 80)
    print("📊 RESUMO DOS TESTES")
    print("=" * 80)
    
    sucessos = sum(1 for r in results if "✅" in r['status'])
    total = len(results)
    total_tokens = sum(r.get('tamanho_resposta', 0) for r in results)
    
    print(f"\nTestes realizados: {total}")
    print(f"Testes bem-sucedidos: {sucessos}")
    print(f"Taxa de sucesso: {(sucessos/total)*100:.2f}%")
    print(f"Total de caracteres gerados: {total_tokens:,}")
    
    print("\nDetalhes por teste:")
    for result in results:
        status_icon = "✅" if "✅" in result['status'] else "❌"
        tamanho = result.get('tamanho_resposta', 0)
        print(f"  {status_icon} {result['teste']:30s} - {tamanho:4d} chars")
        if result['resposta']:
            preview = result['resposta'][:80].replace('\n', ' ')
            print(f"     Preview: {preview}...")
    
    print("\n" + "=" * 80)
    print("✅ TESTE CONCLUÍDO")
    print("=" * 80)


def main():
    """Função principal."""
    try:
        test_enem_questions_api()
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

