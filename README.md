# 🎓 sabia-7b-enem-finetuned

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PEFT](https://img.shields.io/badge/PEFT-0.18.0-green.svg)](https://github.com/huggingface/peft)

Modelo de linguagem fine-tuned do **SABIA-7B** especializado em questões e contexto do **ENEM** (Exame Nacional do Ensino Médio).

## 📋 Sobre o Projeto

Este repositório contém um modelo de linguagem adaptado usando **LoRA (Low-Rank Adaptation)** para ser especializado em:
- ✅ Resolução e análise de questões do ENEM
- ✅ Explicações didáticas sobre Teoria da Resposta ao Item (TRI)
- ✅ Análise de desempenho estudantil
- ✅ Suporte educacional para estudantes do Ensino Médio
- ✅ Geração de conteúdo educacional contextualizado

Desenvolvido pela **XTRI** - Especialista em ENEM/TRI e análise de dados educacionais.

## 🚀 Início Rápido

### Instalação

```bash
# Clone o repositório
git clone https://github.com/xtribr/nlpenem.git
cd nlpenem

# Instale as dependências
pip install -r requirements.txt
```

### Configuração da API (Recomendado)

O modelo usa a **API SABIA-3.1 da Maritaca** ao invés do modelo base local. Configure sua chave de API:

```bash
# Linux/Mac
export MARITACA_API_KEY='sua-chave-aqui'

# Windows (PowerShell)
$env:MARITACA_API_KEY='sua-chave-aqui'

# Ou crie um arquivo .env
echo "MARITACA_API_KEY=sua-chave-aqui" > .env
```

### Uso Básico com API

```python
import os
from maritaca_api import MaritacaAPI

# Inicializar cliente (usa MARITACA_API_KEY do ambiente)
client = MaritacaAPI()

# Gerar resposta para questão ENEM
prompt = "Explique o conceito de Teoria da Resposta ao Item (TRI) no contexto do ENEM:"
response = client.generate_enem_response(prompt, max_tokens=300)
print(response)
```

### Uso Básico (Modo Local - Alternativo)

Se preferir usar o modelo local ao invés da API:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import PeftModel
import torch

# Carregar modelo base e adapter
base_model = "sabia-7b"  # Ajuste para o caminho do modelo base
adapter_path = "./checkpoint-367"

tokenizer = AutoTokenizer.from_pretrained(base_model)
model = AutoModelForCausalLM.from_pretrained(
    base_model,
    torch_dtype=torch.float16,
    device_map="auto"
)
model = PeftModel.from_pretrained(model, adapter_path)

# Gerar resposta
prompt = "Explique o conceito de Teoria da Resposta ao Item (TRI) no contexto do ENEM:"
inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

with torch.no_grad():
    outputs = model.generate(
        **inputs,
        max_new_tokens=256,
        temperature=0.7,
        do_sample=True
    )

response = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(response)
```

Para mais exemplos, consulte:
- [`example_usage.py`](example_usage.py) - Exemplos de uso
- [`test_model_api.py`](test_model_api.py) - Testes com API
- [`maritaca_api.py`](maritaca_api.py) - Cliente da API

## 📊 Métricas de Treinamento

### Resultados Finais
- **Loss Final**: 0.68
- **Token Accuracy**: 84.19%
- **Total de Steps**: 367
- **Epochs**: 1.0

### Evolução do Treinamento

| Step | Loss | Accuracy |
|------|------|----------|
| 25   | 1.12 | 75.13%   |
| 50   | 0.68 | 84.34%   |
| 100  | 0.65 | 84.41%   |
| 200  | 0.65 | 84.36%   |
| 300  | 0.64 | 84.63%   |
| 367  | 0.68 | 84.19%   |

📈 Para análise detalhada, consulte [`ANALISE_TREINAMENTO.md`](ANALISE_TREINAMENTO.md).

## 🔧 Configuração Técnica

### Hiperparâmetros LoRA
- **Rank (r)**: 32
- **Alpha (α)**: 16
- **Dropout**: 0.05
- **Target Modules**: q_proj, k_proj, v_proj, o_proj
- **Bias**: none

### Stack Tecnológico
- **PEFT**: 0.18.0
- **TRL**: 0.25.1
- **Transformers**: 4.57.3
- **PyTorch**: 2.9.1
- **Datasets**: 4.4.1

## 📁 Estrutura do Projeto

```
nlpenem/
├── README.md                 # Este arquivo
├── requirements.txt          # Dependências do projeto
├── .gitignore               # Arquivos ignorados pelo Git
├── example_usage.py         # Exemplos de uso do modelo
├── ANALISE_TREINAMENTO.md   # Análise detalhada do treinamento
├── adapter_config.json      # Configuração do adapter LoRA
├── adapter_model.safetensors # Modelo adapter (LoRA weights)
└── checkpoint-*/            # Checkpoints do treinamento
    ├── checkpoint-100/
    ├── checkpoint-200/
    ├── checkpoint-300/
    └── checkpoint-367/      # Checkpoint final
```

## 📦 Checkpoints Disponíveis

O projeto inclui 4 checkpoints salvos durante o treinamento:

- **checkpoint-100**: Step 100 (Loss: 0.65, Accuracy: 84.41%)
- **checkpoint-200**: Step 200 (Loss: 0.65, Accuracy: 84.36%)
- **checkpoint-300**: Step 300 (Loss: 0.64, Accuracy: 84.63%) ⭐ **Recomendado**
- **checkpoint-367**: Step 367 (Loss: 0.68, Accuracy: 84.19%) - Final

💡 **Recomendação**: O checkpoint-300 apresenta a melhor combinação de métricas (menor loss e maior accuracy).

## 🎯 Casos de Uso

### 1. Resolução de Questões ENEM
```python
questao = """
Questão ENEM: Sobre a Teoria da Resposta ao Item (TRI), assinale a alternativa correta:
A) A TRI não considera o nível de dificuldade dos itens
B) A TRI permite comparar provas de diferentes edições
...
"""
# Gerar resposta e explicação
```

### 2. Análise de Desempenho
```python
notas = {
    "CH": 650.00,
    "CN": 620.00,
    "LC": 680.00,
    "MT": 700.00,
    "Redação": 900.00
}
# Analisar e fornecer orientações
```

### 3. Explicações Didáticas
```python
# Explicar conceitos educacionais de forma didática
prompt = "Explique a diferença entre nota TRI e nota bruta no ENEM:"
```

## ⚠️ Limitações e Considerações

- Este modelo foi fine-tuned para contexto educacional brasileiro e ENEM
- Os resultados devem ser validados por especialistas em educação
- Não substitui estudo tradicional e orientação pedagógica profissional
- Pode conter vieses presentes no dataset de treinamento
- Requer modelo base SABIA-7B para funcionar

## 📝 Licença

Este projeto está licenciado sob a [Apache License 2.0](https://opensource.org/licenses/Apache-2.0).

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📚 Referências e Citações

### TRL (Transformer Reinforcement Learning)
```bibtex
@misc{vonwerra2022trl,
    title        = {{TRL: Transformer Reinforcement Learning}},
    author       = {Leandro von Werra and Younes Belkada and Lewis Tunstall and Edward Beeching and Tristan Thrush and Nathan Lambert and Shengyi Huang and Kashif Rasul and Quentin Gallou{\'e}dec},
    year         = 2020,
    journal      = {GitHub repository},
    publisher    = {GitHub},
    howpublished = {\url{https://github.com/huggingface/trl}}
}
```

### LoRA (Low-Rank Adaptation)
```bibtex
@misc{hu2021lora,
    title={LoRA: Low-Rank Adaptation of Large Language Models},
    author={Edward J. Hu and Yelong Shen and Phillip Wallis and Zeyuan Allen-Zhu and Yuanzhi Li and Shean Wang and Lu Wang and Weizhu Chen},
    year={2021},
    eprint={2106.09685},
    archivePrefix={arXiv},
    primaryClass={cs.CV}
}
```

### SABIA-7B
- Modelo base: [SABIA-7B no Hugging Face](https://huggingface.co/sabia-7b)

## 👥 Autores

- **XTRI** - Especialista em ENEM/TRI e análise de dados educacionais
  - Professor de Ensino Médio
  - CEO da EdTech XTRI (Natal/RN)
  - Trabalha com dados educacionais críticos (190k+ registros)

## 📧 Contato

Para questões, sugestões ou colaborações:
- **GitHub**: [@xtribr](https://github.com/xtribr)
- **Repositório**: [nlpenem](https://github.com/xtribr/nlpenem)

## 🙏 Agradecimentos

- Equipe do Hugging Face pelos frameworks TRL e PEFT
- Desenvolvedores do modelo SABIA-7B
- Comunidade open source de NLP em português

---

⭐ Se este projeto foi útil para você, considere dar uma estrela no repositório!

**Nota**: Este modelo é parte de um projeto educacional focado em análise de dados ENEM e orientação estudantil. Desenvolvido com responsabilidade e compromisso com a educação de qualidade.
