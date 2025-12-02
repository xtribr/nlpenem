"""
Script de validação da estrutura do adapter

Verifica se os arquivos do adapter estão corretos e completos.
"""

import json
from pathlib import Path
import sys


def check_adapter_structure(checkpoint_path: str):
    """Verifica a estrutura de um checkpoint."""
    path = Path(checkpoint_path)
    
    print(f"\n{'='*80}")
    print(f"🔍 Verificando: {checkpoint_path}")
    print(f"{'='*80}\n")
    
    required_files = {
        "adapter_config.json": "Configuração do adapter LoRA",
        "adapter_model.safetensors": "Pesos do adapter (LoRA)",
        "README.md": "Documentação do checkpoint"
    }
    
    optional_files = {
        "tokenizer_config.json": "Configuração do tokenizer",
        "tokenizer.json": "Arquivo do tokenizer",
        "special_tokens_map.json": "Mapeamento de tokens especiais"
    }
    
    results = {
        "checkpoint": checkpoint_path,
        "exists": path.exists(),
        "required_files": {},
        "optional_files": {},
        "config": None,
        "status": "❌"
    }
    
    if not path.exists():
        print(f"❌ Diretório não existe: {checkpoint_path}")
        return results
    
    print("📁 Arquivos obrigatórios:")
    all_required = True
    for file, desc in required_files.items():
        file_path = path / file
        exists = file_path.exists()
        size = file_path.stat().st_size if exists else 0
        size_mb = size / (1024 * 1024)
        
        status = "✅" if exists else "❌"
        print(f"   {status} {file:30s} - {desc}")
        if exists:
            print(f"      Tamanho: {size_mb:.2f} MB")
        
        results["required_files"][file] = {
            "exists": exists,
            "size": size,
            "size_mb": size_mb
        }
        
        if not exists:
            all_required = False
    
    print("\n📁 Arquivos opcionais:")
    for file, desc in optional_files.items():
        file_path = path / file
        exists = file_path.exists()
        status = "✅" if exists else "⚪"
        print(f"   {status} {file:30s} - {desc}")
        results["optional_files"][file] = exists
    
    # Verificar configuração
    print("\n⚙️  Configuração do adapter:")
    config_path = path / "adapter_config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            results["config"] = config
            
            print(f"   ✅ Arquivo de configuração válido")
            print(f"   📊 Parâmetros LoRA:")
            print(f"      - Tipo: {config.get('peft_type', 'N/A')}")
            print(f"      - Rank (r): {config.get('r', 'N/A')}")
            print(f"      - Alpha (α): {config.get('lora_alpha', 'N/A')}")
            print(f"      - Dropout: {config.get('lora_dropout', 'N/A')}")
            print(f"      - Target Modules: {', '.join(config.get('target_modules', []))}")
            print(f"      - Base Model: {config.get('base_model_name_or_path', 'N/A')}")
            
        except Exception as e:
            print(f"   ❌ Erro ao ler configuração: {e}")
    else:
        print("   ❌ Arquivo de configuração não encontrado")
    
    # Status final
    if all_required:
        results["status"] = "✅"
        print(f"\n✅ Checkpoint completo e válido!")
    else:
        print(f"\n❌ Checkpoint incompleto - faltam arquivos obrigatórios")
    
    return results


def main():
    """Função principal."""
    print("=" * 80)
    print("🧪 VALIDAÇÃO DA ESTRUTURA DOS ADAPTERS")
    print("=" * 80)
    
    checkpoints = [
        "checkpoint-100",
        "checkpoint-200", 
        "checkpoint-300",
        "checkpoint-367"
    ]
    
    # Verificar adapter raiz também
    root_adapter = Path("adapter_config.json")
    if root_adapter.exists():
        print("\n📦 Verificando adapter na raiz do projeto...")
        # Simular estrutura
        results_root = {
            "checkpoint": "root",
            "exists": True,
            "required_files": {
                "adapter_config.json": {
                    "exists": True,
                    "size": root_adapter.stat().st_size,
                    "size_mb": root_adapter.stat().st_size / (1024 * 1024)
                }
            },
            "config": None,
            "status": "✅"
        }
        
        try:
            with open(root_adapter, 'r') as f:
                results_root["config"] = json.load(f)
            print("   ✅ adapter_config.json encontrado na raiz")
        except:
            print("   ❌ Erro ao ler adapter_config.json da raiz")
    
    # Verificar todos os checkpoints
    all_results = []
    for checkpoint in checkpoints:
        result = check_adapter_structure(checkpoint)
        all_results.append(result)
    
    # Resumo
    print(f"\n{'='*80}")
    print("📊 RESUMO")
    print(f"{'='*80}\n")
    
    valid = sum(1 for r in all_results if r["status"] == "✅")
    total = len(all_results)
    
    print(f"Checkpoints verificados: {total}")
    print(f"Checkpoints válidos: {valid}")
    print(f"Checkpoints inválidos: {total - valid}\n")
    
    for result in all_results:
        status_icon = "✅" if result["status"] == "✅" else "❌"
        print(f"{status_icon} {result['checkpoint']}")
    
    # Estatísticas de tamanho
    print(f"\n{'='*80}")
    print("📦 ESTATÍSTICAS DE TAMANHO")
    print(f"{'='*80}\n")
    
    for result in all_results:
        if result["status"] == "✅":
            safetensors = result["required_files"].get("adapter_model.safetensors", {})
            if safetensors.get("exists"):
                size_mb = safetensors.get("size_mb", 0)
                print(f"{result['checkpoint']:20s} - {size_mb:8.2f} MB")
    
    # Recomendações
    print(f"\n{'='*80}")
    print("💡 RECOMENDAÇÕES")
    print(f"{'='*80}\n")
    
    if valid == total:
        print("✅ Todos os checkpoints estão completos!")
        print("✅ O modelo está pronto para uso")
        print("\n⚠️  Para testar o modelo completo, você precisa:")
        print("   1. Ter o modelo base SABIA-7B disponível")
        print("   2. Executar: python test_model.py")
        print("   3. Ou usar o exemplo: python example_usage.py")
    else:
        print("⚠️  Alguns checkpoints estão incompletos")
        print("   Verifique os arquivos faltantes acima")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    main()

