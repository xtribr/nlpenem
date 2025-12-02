"""
Exemplo de uso do modelo sabia-7b-enem-finetuned

Este script demonstra como carregar e usar o modelo fine-tuned para questões ENEM.
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel


def load_model(base_model_path: str, adapter_path: str, device: str = "auto"):
    """
    Carrega o modelo base e aplica o adapter LoRA.
    
    Args:
        base_model_path: Caminho para o modelo base SABIA-7B
        adapter_path: Caminho para o adapter LoRA (ex: ./checkpoint-367)
        device: Dispositivo para carregar o modelo ("auto", "cuda", "cpu")
    
    Returns:
        model: Modelo carregado com adapter
        tokenizer: Tokenizer do modelo
    """
    print(f"Carregando tokenizer de {base_model_path}...")
    tokenizer = AutoTokenizer.from_pretrained(base_model_path)
    
    print(f"Carregando modelo base de {base_model_path}...")
    model = AutoModelForCausalLM.from_pretrained(
        base_model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map=device,
        trust_remote_code=True
    )
    
    print(f"Carregando adapter LoRA de {adapter_path}...")
    model = PeftModel.from_pretrained(model, adapter_path)
    model.eval()
    
    print("Modelo carregado com sucesso!")
    return model, tokenizer


def generate_response(
    model,
    tokenizer,
    prompt: str,
    max_new_tokens: int = 256,
    temperature: float = 0.7,
    top_p: float = 0.9,
    do_sample: bool = True
):
    """
    Gera resposta do modelo para um prompt dado.
    
    Args:
        model: Modelo carregado
        tokenizer: Tokenizer do modelo
        prompt: Texto de entrada
        max_new_tokens: Número máximo de tokens a gerar
        temperature: Temperatura para sampling (0.0 = determinístico)
        top_p: Nucleus sampling parameter
        do_sample: Se True, usa sampling; se False, usa greedy decoding
    
    Returns:
        Resposta gerada pelo modelo
    """
    # Tokenizar entrada
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    
    # Gerar resposta
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
    
    # Decodificar resposta
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    # Remover o prompt da resposta (se estiver presente)
    if response.startswith(prompt):
        response = response[len(prompt):].strip()
    
    return response


def exemplo_questao_enem():
    """Exemplo de uso com questão do ENEM."""
    
    # Configurações
    BASE_MODEL = "sabia-7b"  # Ajuste para o caminho correto do modelo base
    ADAPTER_PATH = "./checkpoint-367"  # Ajuste para o checkpoint desejado
    
    # Carregar modelo
    model, tokenizer = load_model(BASE_MODEL, ADAPTER_PATH)
    
    # Exemplo 1: Questão sobre TRI
    prompt1 = """
Questão ENEM: Sobre a Teoria da Resposta ao Item (TRI) utilizada no ENEM, assinale a alternativa correta:

A) A TRI não considera o nível de dificuldade dos itens
B) A TRI permite comparar provas de diferentes edições do exame
C) A TRI utiliza apenas a nota bruta do candidato
D) A TRI não considera o padrão de respostas do candidato
E) A TRI é baseada apenas em estatísticas descritivas simples

Resposta e explicação:
"""
    
    print("=" * 80)
    print("EXEMPLO 1: Questão sobre TRI")
    print("=" * 80)
    resposta1 = generate_response(model, tokenizer, prompt1)
    print(resposta1)
    print("\n")
    
    # Exemplo 2: Explicação de conceito
    prompt2 = """
Explique de forma didática o que é a nota TRI no ENEM e como ela difere da nota bruta:
"""
    
    print("=" * 80)
    print("EXEMPLO 2: Explicação de conceito")
    print("=" * 80)
    resposta2 = generate_response(model, tokenizer, prompt2, max_new_tokens=300)
    print(resposta2)
    print("\n")
    
    # Exemplo 3: Análise de desempenho
    prompt3 = """
Um estudante obteve as seguintes notas no ENEM:
- Ciências Humanas: 650.00
- Ciências da Natureza: 620.00
- Linguagens e Códigos: 680.00
- Matemática: 700.00
- Redação: 900.00

Analise o desempenho deste estudante e forneça orientações:
"""
    
    print("=" * 80)
    print("EXEMPLO 3: Análise de desempenho")
    print("=" * 80)
    resposta3 = generate_response(model, tokenizer, prompt3, max_new_tokens=400)
    print(resposta3)
    print("\n")


if __name__ == "__main__":
    print("=" * 80)
    print("EXEMPLO DE USO - sabia-7b-enem-finetuned")
    print("=" * 80)
    print("\n")
    
    try:
        exemplo_questao_enem()
    except Exception as e:
        print(f"Erro ao executar exemplo: {e}")
        print("\nCertifique-se de que:")
        print("1. O modelo base SABIA-7B está disponível no caminho especificado")
        print("2. O adapter está no caminho './checkpoint-367' ou ajuste ADAPTER_PATH")
        print("3. As dependências estão instaladas (pip install -r requirements.txt)")
        print("4. Há memória GPU/CPU suficiente para carregar o modelo")

