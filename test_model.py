"""
Script de teste do modelo sabia-7b-enem-finetuned

Testa o modelo com questões e exemplos relacionados ao ENEM.
"""

import torch
import sys
from pathlib import Path

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from peft import PeftModel
except ImportError as e:
    print(f"❌ Erro ao importar dependências: {e}")
    print("Instale as dependências com: pip install -r requirements.txt")
    sys.exit(1)


def find_base_model():
    """Tenta encontrar o modelo base em diferentes locais."""
    possible_paths = [
        "sabia-7b",  # Nome do modelo no Hugging Face
        "./sabia-7b",
        "/content/drive/MyDrive/modelos/sabia-7b",  # Caminho original do Colab
        "~/models/sabia-7b",
    ]
    
    # Verificar se é um nome do Hugging Face
    try:
        from transformers import AutoConfig
        config = AutoConfig.from_pretrained("sabia-7b", trust_remote_code=True)
        print("✅ Modelo 'sabia-7b' encontrado no Hugging Face")
        return "sabia-7b"
    except:
        pass
    
    # Verificar caminhos locais
    for path in possible_paths:
        expanded_path = Path(path).expanduser()
        if expanded_path.exists() and expanded_path.is_dir():
            print(f"✅ Modelo encontrado em: {expanded_path}")
            return str(expanded_path)
    
    return None


def load_model_safe(base_model_path: str, adapter_path: str):
    """Carrega o modelo com tratamento de erros."""
    print(f"\n{'='*80}")
    print("🔧 CARREGANDO MODELO")
    print(f"{'='*80}\n")
    
    try:
        print(f"📥 Carregando tokenizer de: {base_model_path}")
        tokenizer = AutoTokenizer.from_pretrained(
            base_model_path,
            trust_remote_code=True
        )
        
        # Configurar pad_token se não existir
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
            print("   ⚠️  pad_token configurado como eos_token")
        
        print(f"📥 Carregando modelo base: {base_model_path}")
        print("   ⏳ Isso pode levar alguns minutos...")
        
        model = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            device_map="auto",
            trust_remote_code=True,
            low_cpu_mem_usage=True
        )
        
        print(f"📥 Carregando adapter LoRA de: {adapter_path}")
        model = PeftModel.from_pretrained(model, adapter_path)
        model.eval()
        
        print("✅ Modelo carregado com sucesso!\n")
        return model, tokenizer
        
    except Exception as e:
        print(f"❌ Erro ao carregar modelo: {e}")
        raise


def generate_response(model, tokenizer, prompt: str, max_new_tokens: int = 256, 
                     temperature: float = 0.7, top_p: float = 0.9):
    """Gera resposta do modelo."""
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    inputs = {k: v.to(model.device) for k, v in inputs.items()}
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
            repetition_penalty=1.1
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remover prompt da resposta
    if response.startswith(prompt):
        response = response[len(prompt):].strip()
    
    return response


def test_enem_questions(model, tokenizer):
    """Testa o modelo com questões do ENEM."""
    print(f"\n{'='*80}")
    print("📝 TESTANDO QUESTÕES ENEM")
    print(f"{'='*80}\n")
    
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
            "max_tokens": 200
        },
        {
            "nome": "Explicação de Nota TRI",
            "prompt": "Explique de forma didática o que é a nota TRI no ENEM e como ela difere da nota bruta:",
            "max_tokens": 300
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
            "max_tokens": 350
        },
        {
            "nome": "Conceito de Média Ponderada",
            "prompt": "Como é calculada a média do ENEM para ingresso em universidades?",
            "max_tokens": 250
        }
    ]
    
    results = []
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'─'*80}")
        print(f"Teste {i}/{len(test_cases)}: {test['nome']}")
        print(f"{'─'*80}\n")
        print(f"Prompt: {test['prompt'][:100]}...\n")
        print("Resposta do modelo:")
        print("─" * 80)
        
        try:
            response = generate_response(
                model, 
                tokenizer, 
                test['prompt'], 
                max_new_tokens=test['max_tokens'],
                temperature=0.7
            )
            
            print(response)
            print("\n")
            
            results.append({
                "teste": test['nome'],
                "status": "✅ Sucesso",
                "resposta": response[:200] + "..." if len(response) > 200 else response
            })
            
        except Exception as e:
            print(f"❌ Erro: {e}\n")
            results.append({
                "teste": test['nome'],
                "status": f"❌ Erro: {str(e)[:50]}",
                "resposta": None
            })
    
    return results


def print_summary(results):
    """Imprime resumo dos testes."""
    print(f"\n{'='*80}")
    print("📊 RESUMO DOS TESTES")
    print(f"{'='*80}\n")
    
    sucessos = sum(1 for r in results if "✅" in r['status'])
    total = len(results)
    
    print(f"Testes realizados: {total}")
    print(f"Testes bem-sucedidos: {sucessos}")
    print(f"Taxa de sucesso: {(sucessos/total)*100:.2f}%\n")
    
    for result in results:
        print(f"{result['status']} - {result['teste']}")
        if result['resposta']:
            print(f"   Preview: {result['resposta'][:100]}...")
        print()


def main():
    """Função principal."""
    print("=" * 80)
    print("🧪 TESTE DO MODELO sabia-7b-enem-finetuned")
    print("=" * 80)
    
    # Verificar dispositivo
    device = "CUDA" if torch.cuda.is_available() else "CPU"
    print(f"\n🖥️  Dispositivo: {device}")
    if torch.cuda.is_available():
        print(f"   GPU: {torch.cuda.get_device_name(0)}")
        print(f"   Memória: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")
    print()
    
    # Encontrar modelo base
    print("🔍 Procurando modelo base...")
    base_model_path = find_base_model()
    
    if not base_model_path:
        print("\n❌ Modelo base não encontrado!")
        print("\nOpções:")
        print("1. Baixar do Hugging Face: o modelo será baixado automaticamente")
        print("2. Especificar caminho local: edite o script e defina BASE_MODEL_PATH")
        print("\nTentando baixar do Hugging Face...")
        base_model_path = "sabia-7b"
    
    # Verificar adapter
    adapter_path = "./checkpoint-367"
    if not Path(adapter_path).exists():
        print(f"\n⚠️  Adapter não encontrado em: {adapter_path}")
        print("Verificando outros checkpoints...")
        for checkpoint in ["checkpoint-300", "checkpoint-200", "checkpoint-100"]:
            if Path(checkpoint).exists():
                adapter_path = f"./{checkpoint}"
                print(f"✅ Usando: {adapter_path}")
                break
        else:
            print("❌ Nenhum checkpoint encontrado!")
            return
    
    try:
        # Carregar modelo
        model, tokenizer = load_model_safe(base_model_path, adapter_path)
        
        # Executar testes
        results = test_enem_questions(model, tokenizer)
        
        # Resumo
        print_summary(results)
        
        print("=" * 80)
        print("✅ TESTE CONCLUÍDO")
        print("=" * 80)
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Teste interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        print("\n💡 Dicas:")
        print("1. Verifique se o modelo base está disponível")
        print("2. Verifique se há memória suficiente (GPU ou RAM)")
        print("3. Instale todas as dependências: pip install -r requirements.txt")


if __name__ == "__main__":
    main()

