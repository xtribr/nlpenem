# 🎓 Guia: Resolução Completa das 3.099 Questões

## ⚠️ Importante

Este processo vai resolver **todas as 3.099 questões** do ENEM usando o modelo. 

**Tempo estimado**: 
- Com intervalo de 0.5s entre requisições: ~25-30 minutos
- Com intervalo de 1s: ~50-60 minutos
- Depende da velocidade da API

## 🚀 Como Executar

### Opção 1: Execução Completa (Recomendado)

```bash
# Executar com intervalo padrão (0.5s)
python resolver_todas_questoes.py

# Executar com intervalo maior (mais seguro para API)
python resolver_todas_questoes.py --intervalo 1.0
```

### Opção 2: Continuar Processamento Interrompido

Se o processo for interrompido, você pode continuar:

```bash
python resolver_todas_questoes.py --continuar
```

O script salva progresso automaticamente a cada 10 questões.

## 📊 O que será gerado

### Estrutura de Arquivos

```
relatorios_treinamento/
├── relatorio_LINGUAGENS.json      # Dados completos de Linguagens
├── relatorio_HUMANAS.json         # Dados completos de Humanas
├── relatorio_NATUREZA.json        # Dados completos de Natureza
├── relatorio_MATEMATICA.json      # Dados completos de Matemática
├── dados_treinamento_linguagens.json  # Formato para treinamento
├── dados_treinamento_humanas.json
├── dados_treinamento_natureza.json
├── dados_treinamento_matematica.json
├── relatorio_geral.json           # Estatísticas gerais
└── RELATORIO_TREINAMENTO.md       # Relatório em Markdown
```

### Conteúdo dos Relatórios

Cada relatório por área contém:
- ✅ Estatísticas (total, acertos, erros, taxa de acerto)
- ✅ Todas as questões resolvidas
- ✅ Respostas do modelo
- ✅ Comparação com gabarito
- ✅ Dados formatados para treinamento

## 📈 Exemplo de Saída

```
📊 Resumo Final:
   LINGUAGENS: 75.50% de acerto (498/661)
   HUMANAS: 72.30% de acerto (588/813)
   NATUREZA: 68.90% de acerto (434/630)
   MATEMATICA: 65.20% de acerto (415/636)
```

## 🔄 Processamento em Background

Para executar em background (Linux/Mac):

```bash
# Executar em background
nohup python resolver_todas_questoes.py --intervalo 1.0 > resolucao.log 2>&1 &

# Acompanhar progresso
tail -f resolucao.log

# Verificar se está rodando
ps aux | grep resolver_todas_questoes
```

## 💾 Progresso Automático

O script salva progresso em:
- `progresso_resolucao.json` - Estado atual do processamento

Se interromper, execute novamente e o script continuará de onde parou.

## ⚙️ Parâmetros

- `--intervalo`: Intervalo entre requisições em segundos (padrão: 0.5)
- `--continuar`: Continuar processamento anterior

## 📝 Notas

1. **Rate Limiting**: A API pode ter limites. Use `--intervalo 1.0` ou maior se houver erros 429
2. **Custos**: Verifique os custos da API antes de processar todas as questões
3. **Tempo**: Reserve tempo suficiente (30-60 minutos)
4. **Backup**: O progresso é salvo automaticamente

---

**Pronto para executar!** 🚀


