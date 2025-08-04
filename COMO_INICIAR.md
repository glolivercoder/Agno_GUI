# 🚀 Como Iniciar o Agno Builder

## Método Mais Simples

```bash
python iniciar_agno.py
```

## Método Manual

```bash
# 1. Ativar ambiente virtual
.\.venv\Scripts\Activate.ps1  # Windows
source .venv/bin/activate     # Linux/Mac

# 2. Iniciar Streamlit
streamlit run agno_builder_interface.py
```

## 🌐 Acessar Interface

Após executar qualquer comando acima, acesse:
**http://localhost:8501**

## ✨ Novas Funcionalidades

### 🔑 APIs Auto-Configuradas
- ✅ **OpenRouter**: Detectado automaticamente
- ✅ **Google Gemini**: Detectado automaticamente  
- ⚠️ **Anthropic**: Não configurado

### 🔌 Nova Aba MCP Tools
- **Gerenciar MCPs**: Visualizar, parar, reiniciar MCPs ativos
- **MCPs Disponíveis**: Lista com 10+ MCPs compatíveis
- **Documentação**: Guia completo sobre MCPs

### 📋 MCPs Sugeridos
- 📁 **Filesystem**: Acesso ao sistema de arquivos
- 🌐 **Fetch**: Requisições HTTP
- 🗄️ **SQLite**: Banco de dados
- 🔧 **Git**: Operações Git
- 🤖 **N8N**: Workflows de automação
- E muito mais...

## 🔧 Solução de Problemas

### ❌ "streamlit command not found"
```bash
pip install streamlit
```

### ❌ "agno not found"
```bash
# Certifique-se de estar no ambiente virtual
.\.venv\Scripts\Activate.ps1
```

### ❌ Interface não abre
- Verifique se a porta 8501 está livre
- Tente: `streamlit run agno_builder_interface.py --server.port 8502`

## 📊 Status das APIs

Baseado no seu arquivo `.env`:
- 🟢 **OpenRouter**: Configurado (sk-or-v1-...)
- 🟢 **Google Gemini**: Configurado (AIzaSy...)
- 🔴 **Anthropic**: Não configurado

## 🎯 Próximos Passos

1. **Inicie a interface**: `python iniciar_agno.py`
2. **Explore a aba MCP**: Configure ferramentas avançadas
3. **Crie seu primeiro agente**: Use as APIs já configuradas
4. **Teste MCPs**: Experimente filesystem ou fetch MCP