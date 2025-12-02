"""
Script de diagnóstico para testar autenticação da API Maritaca
"""

import os
import requests
import json
from pathlib import Path

# Carregar .env
env_path = Path(__file__).parent / '.env'
if env_path.exists():
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                if key.strip() == 'MARITACA_API_KEY':
                    os.environ['MARITACA_API_KEY'] = value.strip()
                    break

api_key = os.getenv("MARITACA_API_KEY")

print("=" * 80)
print("🔍 DIAGNÓSTICO DE AUTENTICAÇÃO - API MARITACA")
print("=" * 80)
print()

if not api_key:
    print("❌ API key não encontrada!")
    exit(1)

print(f"✅ API Key encontrada")
print(f"   Tamanho: {len(api_key)} caracteres")
print(f"   Primeiros 20 chars: {api_key[:20]}...")
print(f"   Últimos 20 chars: ...{api_key[-20:]}")
print()

# Testar diferentes formatos de autenticação
BASE_URL = "https://chat.maritaca.ai/api/chat/completions"

test_cases = [
    {
        "nome": "Formato Bearer (padrão)",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
    },
    {
        "nome": "Formato Bearer com espaços",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": f"Bearer  {api_key}"  # Espaço extra
        }
    },
    {
        "nome": "Formato API-Key",
        "headers": {
            "Content-Type": "application/json",
            "API-Key": api_key
        }
    },
    {
        "nome": "Formato X-API-Key",
        "headers": {
            "Content-Type": "application/json",
            "X-API-Key": api_key
        }
    },
    {
        "nome": "Formato Authorization sem Bearer",
        "headers": {
            "Content-Type": "application/json",
            "Authorization": api_key
        }
    }
]

payload = {
    "model": "sabia-3.1",
    "messages": [
        {
            "role": "user",
            "content": "Olá"
        }
    ],
    "max_tokens": 10
}

print("🧪 Testando diferentes formatos de autenticação...")
print()

for i, test_case in enumerate(test_cases, 1):
    print(f"Teste {i}/{len(test_cases)}: {test_case['nome']}")
    print("-" * 80)
    
    try:
        response = requests.post(
            BASE_URL,
            headers=test_case['headers'],
            json=payload,
            timeout=10
        )
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print(f"   ✅ SUCESSO! Formato correto encontrado!")
            print(f"   Resposta: {response.json()}")
            print()
            print("=" * 80)
            print(f"✅ FORMATO CORRETO: {test_case['nome']}")
            print("=" * 80)
            break
        elif response.status_code == 401:
            print(f"   ❌ 401 Unauthorized")
            try:
                error_detail = response.json()
                print(f"   Detalhes: {error_detail}")
            except:
                print(f"   Resposta: {response.text[:200]}")
        else:
            print(f"   ⚠️  Status: {response.status_code}")
            print(f"   Resposta: {response.text[:200]}")
            
    except Exception as e:
        print(f"   ❌ Erro: {e}")
    
    print()

print()
print("=" * 80)
print("💡 RECOMENDAÇÕES")
print("=" * 80)
print()
print("Se nenhum formato funcionou:")
print("1. Verifique se a API key está correta e ativa")
print("2. Verifique se a API key tem permissões para o modelo sabia-3.1")
print("3. Consulte a documentação da Maritaca: https://docs.maritaca.ai")
print("4. Entre em contato com o suporte da Maritaca")


