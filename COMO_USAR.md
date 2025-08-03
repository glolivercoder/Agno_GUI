# Como Usar o Agno Builder 🚀

## Passo a Passo Rápido

### 1. Configurar Chaves de API

Edite o arquivo `.env` e adicione suas chaves:

```env
# Google Gemini (Gratuito com limites)
GOOGLE_API_KEY=AIzaSy_sua_chave_aqui

# OpenRouter (Tem modelos gratuitos!)
OPENROUTER_API_KEY=sk-or-v1-sua_chave_aqui
```

### 2. Obter as Chaves

**Google Gemini:**
- Acesse: https://makersuite.google.com/app/apikey
- Faça login com sua conta Google
- Clique em "Create API Key"
- Copie a chave e cole no arquivo `.env`

**OpenRouter:**
- Acesse: https://openrouter.ai/keys
- Crie uma conta gratuita
- Clique em "Create Key"
- Copie a chave e cole no arquivo `.env`

### 3. Executar a Interface

```bash
python iniciar_agno_corrigido.py
```

Ou se preferir usar o ambiente virtual manualmente:

```bash
# Windows
.\.venv\Scripts\Activate.ps1
python -m streamlit run agno_builder_simples.py

# Linux/Mac
source .venv/bin/activate
python -m streamlit run agno_builder_simples.py
```

## Modelos Recomendados

### 🆓 Modelos Gratuitos (OpenRouter)
- `meta-llama/llama-3.1-8b-instruct:free` - Llama 3.1 8B
- `mistralai/mistral-7b-instruct:free` - Mistral 7B
- `huggingface/zephyr-7b-beta:free` - Zephyr 7B

### 💰 Modelos Pagos Populares
- `openai/gpt-4o-mini` - GPT-4o Mini (barato)
- `anthropic/claude-3-5-sonnet` - Claude 3.5 Sonnet
- `google/gemini-2.0-flash-exp` - Gemini 2.0 Flash

### 🔴 Google Gemini
- `gemini-2.0-flash-001` - Gemini 2.0 Flash (recomendado)
- `gemini-1.5-pro` - Gemini 1.5 Pro
- `gemini-1.5-flash` - Gemini 1.5 Flash

## Solução de Problemas

### ❌ Erro: "agno not installed"
```bash
# Ative o ambiente virtual primeiro
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Linux/Mac

# Depois execute
python iniciar_agno_corrigido.py
```

### ❌ Erro: "protobuf"
O script corrige automaticamente, mas se persistir:
```bash
pip install protobuf==3.20.3 --force-reinstall
```

### ❌ Erro: "OPENAI_API_KEY must be set"
Para OpenRouter, você precisa configurar:
```env
OPENROUTER_API_KEY=sk-or-v1-sua_chave
```

### ❌ Erro: "google.genai not found"
```bash
pip install google-genai google-generativeai
```

## Testando a Configuração

Execute o teste específico:
```bash
python exemplo_configuracao_modelos.py
```

Este script vai:
- ✅ Verificar se as chaves estão configuradas
- 🧪 Testar cada provedor
- 📋 Mostrar modelos disponíveis
- 🎯 Comparar respostas

## Dicas Importantes

1. **Use o Ambiente Virtual**: Sempre ative `.venv` antes de executar
2. **Modelos Gratuitos**: OpenRouter tem vários modelos gratuitos
3. **Gemini Gratuito**: Google Gemini tem cota gratuita generosa
4. **Custos**: Sempre verifique os preços em https://openrouter.ai/models
5. **Protobuf**: Se der erro, use `protobuf==3.20.3`

## Estrutura de Arquivos

```
agno/
├── .venv/                    # Ambiente virtual
├── .env                      # Suas chaves de API
├── agno_builder_simples.py   # Interface principal
├── iniciar_agno_corrigido.py # Script de inicialização
├── exemplo_configuracao_modelos.py # Teste de configuração
└── COMO_USAR.md             # Este arquivo
```

## Suporte

Se ainda tiver problemas:

1. Verifique se está no ambiente virtual correto
2. Execute `python exemplo_configuracao_modelos.py` para diagnóstico
3. Verifique se as chaves de API estão corretas no arquivo `.env`
4. Certifique-se de que o protobuf está na versão 3.20.3

## Links Úteis

- 📚 Documentação Agno: https://docs.agno.com
- 🔑 Chaves Google: https://makersuite.google.com/app/apikey
- 🌐 Chaves OpenRouter: https://openrouter.ai/keys
- 💰 Preços OpenRouter: https://openrouter.ai/models
- 🤖 Modelos Disponíveis: https://openrouter.ai/models