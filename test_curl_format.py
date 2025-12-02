"""
Teste direto da API usando o mesmo formato do curl
"""

import os
import requests
import json
from pathlib import Path

# Carregar .env
env_path = Path(__file__).parent / '.env'
api_key = None

if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() == 'MARITACA_API_KEY':
                    api_key = value.strip()
                    break

if not api_key:
    print("❌ API key não encontrada no .env")
    exit(1)

print("=" * 80)
print("🧪 TESTE DIRETO DA API (formato curl)")
print("=" * 80)
print()
print(f"API Key (primeiros 20 chars): {api_key[:20]}...")
print(f"Tamanho: {len(api_key)} caracteres")
print()

# Testar exatamente como no curl
url = "https://chat.maritaca.ai/api/chat/completions"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

payload = {
    "model": "sabia-3.1",
    "messages": [
        {
            "role": "user",
            "content": "Olá, Mundo!"
        }
    ]
}

print("📤 Enviando requisição...")
print(f"   URL: {url}")
print(f"   Headers: {json.dumps(headers, indent=2)}")
print(f"   Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
print()

try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    print(f"📥 Resposta recebida:")
    print(f"   Status Code: {response.status_code}")
    print()
    
    if response.status_code == 200:
        print("✅ SUCESSO!")
        data = response.json()
        print(f"   Resposta: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        if "choices" in data and len(data["choices"]) > 0:
            content = data["choices"][0]["message"]["content"]
            print()
            print(f"💬 Conteúdo: {content}")
    else:
        print("❌ ERRO!")
        print(f"   Status: {response.status_code}")
        print(f"   Resposta: {response.text}")
        
        # Tentar parsear erro
        try:
            error_data = response.json()
            print(f"   Erro JSON: {json.dumps(error_data, indent=2, ensure_ascii=False)}")
        except:
            pass

except Exception as e:
    print(f"❌ Exceção: {e}")
    import traceback
    traceback.print_exc()


