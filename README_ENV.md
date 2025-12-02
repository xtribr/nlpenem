# 🔐 Configuração da API Key no .env

A API key da Maritaca está configurada no arquivo `.env` e será carregada automaticamente por todos os scripts.

## ✅ Configuração Atual

A API key já está salva no arquivo `.env`:
```
MARITACA_API_KEY=107341642936117619902_14127420ffa6b338
```

## 🔄 Como Funciona

Todos os scripts agora carregam automaticamente a API key do arquivo `.env`:

1. **maritaca_api.py** - Carrega automaticamente na importação
2. **resolver_questoes_enem.py** - Busca no .env se não encontrar na env var
3. **demo_questoes_enem.py** - Busca no .env se não encontrar na env var
4. **test_model_api.py** - Busca no .env se não encontrar na env var
5. **example_usage.py** - Busca no .env se não encontrar na env var

## 🚀 Uso

Agora você pode usar os scripts sem precisar configurar variáveis de ambiente:

```bash
# Resolver questões
python demo_questoes_enem.py -r -n 5

# Testar modelo
python test_model_api.py

# Exemplo de uso
python example_usage.py
```

## 🔒 Segurança

O arquivo `.env` está no `.gitignore` e **NÃO será commitado** no Git.

⚠️ **Importante**: Nunca compartilhe sua API key publicamente!

## 📝 Atualizar API Key

Se precisar atualizar a API key, edite o arquivo `.env`:

```bash
# Editar .env
nano .env

# Ou usar echo
echo "MARITACA_API_KEY=nova-chave-aqui" > .env
```

## ✅ Verificação

Para verificar se a API key está sendo carregada:

```python
from maritaca_api import MaritacaAPI

client = MaritacaAPI()
print("✅ API key carregada com sucesso!")
```

---

**Status**: ✅ Configurado e funcionando


