"""
Exemplo de uso do modelo sabia-7b-enem-finetuned

Este script demonstra como usar o modelo fine-tuned para questões ENEM.
Agora usando API SABIA-3.1 da Maritaca ao invés do modelo local SABIA-7B.
"""

import os
import sys
from pathlib import Path

# Adicionar diretório atual ao path
sys.path.insert(0, str(Path(__file__).parent))

# Tentar importar API
try:
    from maritaca_api import MaritacaAPI
    USE_API = True
except ImportError:
    USE_API = False
    print("⚠️  maritaca_api.py não encontrado. Instale requests: pip install requests")


def exemplo_questao_enem_api():
    """Exemplo de uso com API SABIA-3.1 da Maritaca."""
    
    # Verificar API key
    api_key = os.getenv("MARITACA_API_KEY")
    if not api_key:
        print("❌ Erro: MARITACA_API_KEY não encontrada!")
        print("\nConfigure a variável de ambiente:")
        print("  export MARITACA_API_KEY='sua-chave-aqui'")
        return
    
    # Inicializar cliente
    try:
        client = MaritacaAPI(api_key=api_key)
        print("✅ Cliente API inicializado com sucesso!\n")
    except Exception as e:
        print(f"❌ Erro ao inicializar cliente: {e}")
        return
    
    # Exemplo 1: Questão sobre TRI
    prompt1 = """Questão ENEM: Sobre a Teoria da Resposta ao Item (TRI) utilizada no ENEM, assinale a alternativa correta:

A) A TRI não considera o nível de dificuldade dos itens
B) A TRI permite comparar provas de diferentes edições do exame
C) A TRI utiliza apenas a nota bruta do candidato
D) A TRI não considera o padrão de respostas do candidato
E) A TRI é baseada apenas em estatísticas descritivas simples

Resposta e explicação:"""
    
    print("=" * 80)
    print("EXEMPLO 1: Questão sobre TRI")
    print("=" * 80)
    try:
        resposta1 = client.generate_enem_response(prompt1, max_tokens=300)
        print(resposta1)
    except Exception as e:
        print(f"❌ Erro: {e}")
    print("\n")
    
    # Exemplo 2: Explicação de conceito
    prompt2 = "Explique de forma didática o que é a nota TRI no ENEM e como ela difere da nota bruta:"
    
    print("=" * 80)
    print("EXEMPLO 2: Explicação de conceito")
    print("=" * 80)
    try:
        resposta2 = client.generate_enem_response(prompt2, max_tokens=400)
        print(resposta2)
    except Exception as e:
        print(f"❌ Erro: {e}")
    print("\n")
    
    # Exemplo 3: Análise de desempenho
    prompt3 = """Um estudante obteve as seguintes notas no ENEM:
- Ciências Humanas: 650.00
- Ciências da Natureza: 620.00
- Linguagens e Códigos: 680.00
- Matemática: 700.00
- Redação: 900.00

Analise o desempenho deste estudante e forneça orientações:"""
    
    print("=" * 80)
    print("EXEMPLO 3: Análise de desempenho")
    print("=" * 80)
    try:
        resposta3 = client.generate_enem_response(prompt3, max_tokens=500)
        print(resposta3)
    except Exception as e:
        print(f"❌ Erro: {e}")
    print("\n")


def exemplo_questao_enem_local():
    """Exemplo de uso com modelo local (fallback se API não disponível)."""
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer
        from peft import PeftModel
    except ImportError:
        print("❌ Dependências não instaladas. Execute: pip install torch transformers peft")
        return
    
    # Configurações
    BASE_MODEL = "sabia-7b"  # Ajuste para o caminho correto do modelo base
    ADAPTER_PATH = "./checkpoint-367"  # Ajuste para o checkpoint desejado
    
    print("⚠️  Usando modo local (requer modelo base SABIA-7B)")
    print("💡 Recomendado: Use a API com MARITACA_API_KEY configurada\n")
    
    try:
        # Carregar modelo
        print(f"Carregando tokenizer de {BASE_MODEL}...")
        tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL, trust_remote_code=True)
        
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        print(f"Carregando modelo base: {BASE_MODEL}...")
        model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True
        )
        
        print(f"Carregando adapter LoRA de {ADAPTER_PATH}...")
        model = PeftModel.from_pretrained(model, ADAPTER_PATH)
        model.eval()
        print("✅ Modelo carregado!\n")
        
        # Exemplos (mesmos prompts)
        # ... (código similar ao anterior)
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo local: {e}")
        print("\n💡 Use a API ao invés do modelo local:")
        print("   export MARITACA_API_KEY='sua-chave'")
        print("   python example_usage.py")


def main():
    """Função principal - tenta usar API, fallback para local."""
    print("=" * 80)
    print("EXEMPLO DE USO - sabia-7b-enem-finetuned")
    print("=" * 80)
    print("\n")
    
    # Priorizar API
    if USE_API:
        # Tentar carregar do .env se não estiver na env var
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
        
        if api_key:
            print("✅ Usando API SABIA-3.1 da Maritaca\n")
            exemplo_questao_enem_api()
            return
        else:
            print("⚠️  MARITACA_API_KEY não configurada")
            print("💡 Configure: export MARITACA_API_KEY='sua-chave'\n")
    
    # Fallback para local
    print("Tentando modo local...\n")
    exemplo_questao_enem_local()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
