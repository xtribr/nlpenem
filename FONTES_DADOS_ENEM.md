# 📚 Fontes de Dados do ENEM em JSON

Este documento lista todas as fontes disponíveis para obter provas e questões do ENEM em formato JSON/JSONL.

## 🎯 Fontes Identificadas

### 1. Google Drive (Dataset Completo) ⭐ **USADO NO TREINAMENTO**

**Localização**: Pasta do Google Drive  
**ID da Pasta**: `1datullhe8eo6Ogi5zVV04TJyRl314eDZ`  
**Formato**: JSONL (JSON Lines)  
**Quantidade**: 21 arquivos (2012-2023)

**Arquivos**:
- `enem_2012_completo.jsonl`
- `enem_2013_completo.jsonl`
- ...
- `enem_2023_completo.jsonl`

**Como baixar**:
```bash
# Instalar gdown
pip install gdown

# Baixar pasta completa
gdown --folder 1datullhe8eo6Ogi5zVV04TJyRl314eDZ -O enem_dados
```

**Ou usar o script**:
```bash
python download_enem_data.py
```

### 2. API ENEM (enem.dev) 🌐

**URL**: https://api.enem.dev  
**Formato**: JSON (REST API)  
**Quantidade**: Mais de 2.700 questões  
**Anos**: 2009-2023

**Endpoints**:
- `GET /questions` - Lista todas as questões
- `GET /questions/{id}` - Questão específica
- `GET /questions?year={ano}` - Questões por ano
- `GET /questions?subject={area}` - Questões por área

**Exemplo de uso**:
```python
import requests

# Buscar questões
response = requests.get("https://api.enem.dev/questions")
questoes = response.json()

# Buscar por ano
response = requests.get("https://api.enem.dev/questions?year=2023")
questoes_2023 = response.json()
```

**Documentação**: https://enem.dev

### 3. Microdados INEP (Dados Oficiais) 📊

**URL**: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem  
**Formato**: CSV, TXT, DTA (Stata)  
**Quantidade**: Dados completos de todos os participantes  
**Anos**: Desde 1998

**Conteúdo**:
- Respostas dos participantes
- Notas TRI
- Informações demográficas
- Gabaritos oficiais

**Como converter para JSON**:
```python
import pandas as pd
import json

# Ler microdados
df = pd.read_csv("microdados_enem_2023.csv", encoding='latin-1', sep=';')

# Converter para JSON
df.to_json("enem_2023.json", orient='records', force_ascii=False)
```

### 4. Hugging Face Datasets 🤗

Alguns datasets do ENEM estão disponíveis no Hugging Face:

- Pesquisar: https://huggingface.co/datasets?search=enem
- Exemplos:
  - `enem_questions`
  - `enem_brasil`

**Como usar**:
```python
from datasets import load_dataset

dataset = load_dataset("nome_do_dataset_enem")
```

## 📋 Estrutura dos Dados

### Formato JSONL (Google Drive)

Cada linha é um JSON com uma questão:

```json
{
  "ano": 2023,
  "area": "Matemática",
  "questao": "Texto da questão...",
  "alternativas": {
    "A": "Alternativa A",
    "B": "Alternativa B",
    "C": "Alternativa C",
    "D": "Alternativa D",
    "E": "Alternativa E"
  },
  "gabarito": "C",
  "tema": "Álgebra",
  "dificuldade": "Média"
}
```

### Formato API ENEM

```json
{
  "id": "12345",
  "year": 2023,
  "subject": "Matemática",
  "question": "Texto da questão...",
  "alternatives": [...],
  "correct_answer": "C",
  "topic": "Álgebra"
}
```

## 🔧 Scripts Disponíveis

### `download_enem_data.py`

Script completo para:
- ✅ Baixar do Google Drive
- ✅ Buscar da API ENEM
- ✅ Processar e converter formatos
- ✅ Gerar estatísticas

**Uso**:
```bash
python download_enem_data.py
```

## 📊 Estatísticas dos Dados

### Dataset Google Drive
- **Total de arquivos**: 21
- **Período**: 2012-2023
- **Formato**: JSONL
- **Estimativa**: ~2.000+ questões por ano = ~20.000+ questões totais

### API ENEM
- **Total de questões**: 2.700+
- **Anos**: 2009-2023
- **Áreas**: CH, CN, LC, MT, Redação

## 🎯 Recomendações de Uso

### Para Treinamento
1. **Google Drive Dataset** (recomendado)
   - Mais completo
   - Já usado no treinamento atual
   - Formato JSONL eficiente

### Para Testes Rápidos
2. **API ENEM**
   - Fácil acesso
   - Sem necessidade de download
   - Atualizado regularmente

### Para Análises Estatísticas
3. **Microdados INEP**
   - Dados oficiais completos
   - Inclui respostas dos participantes
   - Requer processamento adicional

## ⚠️ Considerações

1. **Licença**: Verificar licença de cada fonte
2. **Atualização**: APIs podem ter rate limits
3. **Qualidade**: Validar dados antes de usar
4. **Privacidade**: Microdados do INEP são anonimizados

## 🔗 Links Úteis

- **API ENEM**: https://enem.dev
- **Microdados INEP**: https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/enem
- **Hugging Face**: https://huggingface.co/datasets

---

**Última atualização**: 2025-01-27


