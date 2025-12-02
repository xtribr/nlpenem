# 📊 Análise Completa das Provas do ENEM

**Data da Análise**: 2025-01-27  
**Total de Arquivos**: 21 arquivos JSONL  
**Período**: 2009-2025

## 📈 Resumo Executivo

- **Total de Questões**: 3.099 questões
- **Total de Arquivos**: 21 arquivos
- **Tamanho Total**: ~4.0 MB
- **Média de Questões por Arquivo**: 147.57
- **Mediana**: 174 questões por arquivo

## 📅 Distribuição por Ano

| Ano | Arquivos | Questões |
|-----|----------|----------|
| 2009 | enem_2009_completo.jsonl | 174 |
| 2010 | enem_2010_completo.jsonl | 184 |
| 2011 | enem_2011_completo.jsonl | 185 |
| 2012 | enem_2012_completo.jsonl | 182 |
| 2013 | enem_2013_completo.jsonl | 180 |
| 2014 | enem_2014_completo.jsonl | 164 |
| 2015 | enem_2015_completo.jsonl | 169 |
| 2016 | enem_2016_completo.jsonl | 161 |
| 2017 | enem_2017_completo.jsonl | 182 |
| 2018 | enem_2018_completo.jsonl | 174 |
| 2019 | enem_2019_completo.jsonl | 165 |
| 2020 | enem_2020_completo.jsonl | 179 |
| 2021 | enem_2021_completo.jsonl | 183 |
| 2022 | enem_2022_completo.jsonl | 179 |
| 2023 | enem_2023_completo.jsonl | 138 |
| 2024 | enem_2024_completo.jsonl | 180 |
| 2025 | enem_2025_completo.jsonl + 4 arquivos específicos | 320 |

## 📚 Distribuição por Área de Conhecimento

| Área | Questões | Percentual |
|------|----------|------------|
| **Ciências Humanas** (human-sciences) | 813 | 26.23% |
| **Linguagens e Códigos** (languages) | 661 | 21.33% |
| **Matemática** (mathematics) | 636 | 20.52% |
| **Ciências da Natureza** (natural-sciences) | 630 | 20.33% |
| **Não especificado** | 359 | 11.58% |

### Observações

- Distribuição equilibrada entre as 4 áreas principais
- Ciências Humanas tem ligeiramente mais questões
- Arquivos de 2025 incluem separação por área (4 arquivos específicos)

## 📋 Estrutura dos Dados

### Campos Identificados

Cada questão contém os seguintes campos:

- **Identificação**: `id`, `number`, `label`, `exam`
- **Conteúdo**: `question`, `original_question`, `description`, `context`
- **Alternativas**: `alternatives`, `alternatives_type`, `options`, `answer`
- **Classificação**: `area`, `subject`
- **Imagens**: `has_images`, `has_associated_images`, `figures`, `associated_images`, `context_images`, `image_description`
- **Metadados**: `incomplete`, `ledor`, `BK`, `CE`, `DS`, `IU`, `ML`, `MR`, `TU`

### Formato das Questões

```json
{
  "id": "...",
  "number": 1,
  "exam": "ENEM",
  "area": "mathematics",
  "subject": "Matemática",
  "question": "Texto da questão...",
  "alternatives": {
    "A": "...",
    "B": "...",
    "C": "...",
    "D": "...",
    "E": "..."
  },
  "answer": "C",
  "context": "...",
  "has_images": false,
  ...
}
```

## 📊 Estatísticas Detalhadas

### Por Arquivo

| Arquivo | Questões | Tamanho (MB) |
|---------|----------|--------------|
| enem_2011_completo.jsonl | 185 | 0.21 |
| enem_2010_completo.jsonl | 184 | 0.22 |
| enem_2021_completo.jsonl | 183 | 0.21 |
| enem_2012_completo.jsonl | 182 | 0.20 |
| enem_2017_completo.jsonl | 182 | 0.20 |
| enem_2013_completo.jsonl | 180 | 0.18 |
| enem_2024_completo.jsonl | 180 | 0.23 |
| enem_2020_completo.jsonl | 179 | 0.20 |
| enem_2022_completo.jsonl | 179 | 0.43 |
| enem_2009_completo.jsonl | 174 | 0.23 |
| enem_2018_completo.jsonl | 174 | 0.19 |
| enem_2015_completo.jsonl | 169 | 0.17 |
| enem_2019_completo.jsonl | 165 | 0.18 |
| enem_2014_completo.jsonl | 164 | 0.17 |
| enem_2016_completo.jsonl | 161 | 0.16 |
| enem_2025_completo.jsonl | 160 | 0.11 |
| enem_2023_completo.jsonl | 138 | 0.16 |
| enem_2025_human-sciences.jsonl | 45 | 0.04 |
| enem_2025_mathematics.jsonl | 45 | 0.02 |
| enem_2025_natural-sciences.jsonl | 45 | 0.02 |
| enem_2025_languages.jsonl | 25 | 0.03 |

### Estatísticas Numéricas

- **Média de questões por arquivo**: 147.57
- **Mediana**: 174 questões
- **Mínimo**: 25 questões (enem_2025_languages.jsonl)
- **Máximo**: 185 questões (enem_2011_completo.jsonl)
- **Desvio padrão**: ~45 questões

## 🎯 Características Especiais

### Arquivos de 2025

O ano de 2025 possui uma estrutura especial:
- **enem_2025_completo.jsonl**: 160 questões (arquivo completo)
- **enem_2025_human-sciences.jsonl**: 45 questões (apenas CH)
- **enem_2025_languages.jsonl**: 25 questões (apenas LC)
- **enem_2025_mathematics.jsonl**: 45 questões (apenas MT)
- **enem_2025_natural-sciences.jsonl**: 45 questões (apenas CN)

**Total 2025**: 320 questões

## 📝 Observações Importantes

1. **Campos de Ano**: Os arquivos não possuem campo `ano` explícito, mas o ano está no nome do arquivo
2. **Dificuldade**: Campo `dificuldade` não está presente nos dados
3. **Temas**: Campo `tema` não está presente nos dados
4. **Imagens**: Algumas questões possuem campos relacionados a imagens (`has_images`, `figures`, etc.)
5. **Formato**: Todas as questões estão em formato JSONL (uma por linha)

## 🔧 Uso no Projeto

### Scripts Atualizados

- ✅ `download_enem_data.py` - Usa pasta `provas/`
- ✅ `resolver_questoes_enem.py` - Busca em `provas/`
- ✅ `analisar_provas_enem.py` - Analisa `provas/`

### Como Usar

```python
from pathlib import Path
import json

# Carregar questões
pasta_provas = Path("provas")
arquivo = pasta_provas / "enem_2023_completo.jsonl"

with open(arquivo, 'r', encoding='utf-8') as f:
    for linha in f:
        questao = json.loads(linha.strip())
        print(questao['question'])
```

## 📊 Arquivo de Estatísticas

As estatísticas completas foram salvas em:
- **`estatisticas_provas_enem.json`** - Dados completos em JSON

## ✅ Status

- ✅ 21 arquivos indexados
- ✅ 3.099 questões analisadas
- ✅ Estatísticas geradas
- ✅ Scripts atualizados para usar pasta `provas/`
- ✅ Documentação criada

---

**Última atualização**: 2025-01-27

