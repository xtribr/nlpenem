# 🔧 Configuração da API Maritaca

Este guia explica como configurar e usar a API SABIA-3.1 da Maritaca com o modelo fine-tuned.

## 📋 Pré-requisitos

1. **Chave de API da Maritaca**
   - Obtenha sua chave em: https://maritaca.ai
   - A chave deve ter acesso ao modelo `sabia-3.1`

2. **Dependências instaladas**
   ```bash
   pip install requests
   ```

## 🔑 Configuração da Chave de API

### Opção 1: Variável de Ambiente (Recomendado)

**Linux/Mac:**
```bash
export MARITACA_API_KEY='sua-chave-aqui'
```

**Windows (PowerShell):**
```powershell
$env:MARITACA_API_KEY='sua-chave-aqui'
```

**Windows (CMD):**
```cmd
set MARITACA_API_KEY=sua-chave-aqui
```

### Opção 2: Arquivo .env

Crie um arquivo `.env` na raiz do projeto:

```bash
echo "MARITACA_API_KEY=sua-chave-aqui" > .env
```

E carregue no Python:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Opção 3: Passar Diretamente no Código

```python
from maritaca_api import MaritacaAPI

client = MaritacaAPI(api_key="sua-chave-aqui")
```

⚠️ **Não commite a chave no Git!** Use variáveis de ambiente.

## 🧪 Testando a Configuração

### Teste Rápido

```python
from maritaca_api import MaritacaAPI, test_api_connection

# Testar conexão
if test_api_connection():
    print("✅ API configurada corretamente!")
else:
    print("❌ Erro na configuração da API")
```

### Teste Completo

```bash
python test_model_api.py
```

Este script testa a API com várias questões ENEM e mostra os resultados.

## 📝 Exemplo de Uso

```python
import os
from maritaca_api import MaritacaAPI

# Verificar se a chave está configurada
api_key = os.getenv("MARITACA_API_KEY")
if not api_key:
    print("❌ MARITACA_API_KEY não encontrada!")
    exit(1)

# Inicializar cliente
client = MaritacaAPI(api_key=api_key)

# Gerar resposta para questão ENEM
prompt = """
Questão ENEM: Sobre a Teoria da Resposta ao Item (TRI), assinale a alternativa correta:
A) A TRI não considera o nível de dificuldade dos itens
B) A TRI permite comparar provas de diferentes edições
...
"""

response = client.generate_enem_response(
    prompt=prompt,
    temperature=0.7,
    max_tokens=300
)

print(response)
```

## 🔍 Solução de Problemas

### Erro: "API key não fornecida"

**Causa**: A variável `MARITACA_API_KEY` não está configurada.

**Solução**:
```bash
export MARITACA_API_KEY='sua-chave'
# Verificar
echo $MARITACA_API_KEY
```

### Erro: "401 Unauthorized"

**Causa**: Chave de API inválida ou expirada.

**Solução**:
1. Verifique se a chave está correta
2. Verifique se a chave tem acesso ao modelo `sabia-3.1`
3. Gere uma nova chave se necessário

### Erro: "Connection timeout"

**Causa**: Problema de conexão com a API.

**Solução**:
1. Verifique sua conexão com a internet
2. Verifique se a API da Maritaca está online
3. Tente novamente após alguns segundos

### Erro: "ModuleNotFoundError: No module named 'requests'"

**Causa**: Biblioteca `requests` não instalada.

**Solução**:
```bash
pip install requests
```

## 📊 Parâmetros da API

### Parâmetros Disponíveis

- **model**: `"sabia-3.1"` (fixo)
- **temperature**: 0.0 - 2.0 (padrão: 0.7)
- **max_tokens**: 1 - 4096 (padrão: 512)
- **top_p**: 0.0 - 1.0 (padrão: 0.9)
- **stream**: True/False (padrão: False)

### Exemplo com Parâmetros Customizados

```python
response = client.generate(
    prompt="Sua pergunta aqui",
    temperature=0.5,  # Mais determinístico
    max_tokens=1000,  # Respostas mais longas
    top_p=0.95        # Mais diversidade
)
```

## 🔐 Segurança

### Boas Práticas

1. ✅ **Nunca commite a chave no Git**
   - Adicione `.env` ao `.gitignore`
   - Use variáveis de ambiente

2. ✅ **Use chaves diferentes para dev/prod**
   - Desenvolvimento: chave de teste
   - Produção: chave com limites apropriados

3. ✅ **Rotacione chaves regularmente**
   - Gere novas chaves periodicamente
   - Revogue chaves antigas não utilizadas

4. ✅ **Monitore uso da API**
   - Acompanhe custos e limites
   - Configure alertas se necessário

## 📚 Recursos Adicionais

- **Documentação da API Maritaca**: https://docs.maritaca.ai
- **Exemplos de uso**: Veja `example_usage.py`
- **Testes**: Execute `python test_model_api.py`

## 💡 Dicas

1. **Cache de respostas**: Para questões similares, considere implementar cache
2. **Rate limiting**: Respeite os limites da API
3. **Tratamento de erros**: Sempre trate exceções ao chamar a API
4. **Logging**: Registre chamadas para debug e monitoramento

---

**Pronto!** Agora você pode usar a API SABIA-3.1 da Maritaca com o modelo fine-tuned para ENEM.


