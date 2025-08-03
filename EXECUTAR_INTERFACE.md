# 🚀 Como Executar a Interface Agno Builder

## ⚠️ Problema Identificado

O erro `missing ScriptRunContext` ocorre quando o Streamlit é inicializado fora do contexto adequado. Isso acontece porque o código estava tentando configurar o Streamlit durante a importação da classe.

## ✅ Solução Implementada

Criei um script de inicialização separado que resolve o problema:

### **Método 1: Usar o Script de Inicialização (Recomendado)**

```bash
# Execute este comando:
streamlit run iniciar_agno_builder.py
```

### **Método 2: Executar Diretamente (Alternativo)**

```bash
# Se ainda quiser usar o arquivo original:
streamlit run agno_builder_interface.py
```

## 🔧 Pré-requisitos

### **1. Instalar Dependências**

```bash
# Dependências básicas
pip install streamlit agno

# Provedores de modelos (instale os que for usar)
pip install openai anthropic google-generativeai
```

### **2. Configurar Chaves de API**

Configure apenas as chaves dos provedores que pretende usar:

#### **Windows (PowerShell)**
```powershell
$env:OPENAI_API_KEY="sua_chave_openai"
$env:ANTHROPIC_API_KEY="sua_chave_anthropic"
$env:GOOGLE_API_KEY="sua_chave_google"
$env:OPENROUTER_API_KEY="sua_chave_openrouter"
```

#### **Linux/Mac (Bash)**
```bash
export OPENAI_API_KEY="sua_chave_openai"
export ANTHROPIC_API_KEY="sua_chave_anthropic"
export GOOGLE_API_KEY="sua_chave_google"
export OPENROUTER_API_KEY="sua_chave_openrouter"
```

#### **Arquivo .env (Opcional)**
```env
OPENAI_API_KEY=sua_chave_openai
ANTHROPIC_API_KEY=sua_chave_anthropic
GOOGLE_API_KEY=sua_chave_google
OPENROUTER_API_KEY=sua_chave_openrouter
```

## 🌐 Obter Chaves de API

### **OpenAI**
- Site: https://platform.openai.com/api-keys
- Modelos: GPT-4, GPT-3.5, GPT-4o
- Custo: Pago por uso

### **Anthropic**
- Site: https://console.anthropic.com/
- Modelos: Claude 3.5 Sonnet, Opus, Haiku
- Custo: Pago por uso

### **Google Gemini**
- Site: https://makersuite.google.com/app/apikey
- Modelos: Gemini 2.0 Flash, Pro
- Custo: Gratuito com limites, pago para uso intenso

### **OpenRouter**
- Site: https://openrouter.ai/keys
- Modelos: 100+ modelos de diferentes provedores
- Custo: Varia (muitos modelos gratuitos disponíveis)

## 🎯 Execução Passo a Passo

### **1. Verificar Instalação**
```bash
# Testar se o Agno está instalado
python -c "import agno; print('✅ Agno instalado com sucesso')"

# Testar se o Streamlit está instalado
streamlit --version
```

### **2. Executar Interface**
```bash
# Navegar para o diretório do projeto
cd caminho/para/agno_gui

# Executar a interface
streamlit run iniciar_agno_builder.py
```

### **3. Acessar no Navegador**
A interface será aberta automaticamente em:
- **URL**: http://localhost:8501
- **Porta**: 8501 (padrão do Streamlit)

## 🔍 Solução de Problemas

### **Erro: "missing ScriptRunContext"**
✅ **Solução**: Use `streamlit run iniciar_agno_builder.py` em vez do arquivo original

### **Erro: "ModuleNotFoundError: No module named 'agno'"**
✅ **Solução**: 
```bash
pip install agno
```

### **Erro: "No module named 'openai'"**
✅ **Solução**: 
```bash
pip install openai anthropic google-generativeai
```

### **Erro: "API key not configured"**
✅ **Solução**: Configure as chaves de API conforme mostrado acima

### **Interface não carrega**
✅ **Soluções**:
1. Verifique se está no diretório correto
2. Certifique-se de que o ambiente virtual está ativado
3. Tente executar: `streamlit run iniciar_agno_builder.py --server.port 8502`

### **Erro de importação do Agno**
✅ **Solução**: 
```bash
# Reinstalar o Agno
pip uninstall agno
pip install agno

# Ou instalar versão específica
pip install agno==1.7.7
```

## 📱 Usando a Interface

### **1. Seleção de Nível**
- Use a barra lateral para escolher entre os 5 níveis
- Cada nível tem funcionalidades específicas

### **2. Configuração de Modelos**
- Escolha o provedor (OpenAI, Anthropic, Google, OpenRouter)
- Selecione o modelo específico
- Configure parâmetros avançados

### **3. Ferramentas e Recursos**
- Selecione ferramentas usando checkboxes
- Configure instruções personalizadas
- Use templates pré-configurados

### **4. Geração de Código**
- Clique em "🔄 Gerar Código" para ver o Python
- Use "📤 Exportar Código" para download
- Teste o código gerado em seu ambiente

## 🎉 Sucesso!

Se tudo estiver configurado corretamente, você verá:

```
🤖 Agno Agent Builder
========================

✅ Agno Framework carregado
✅ Streamlit inicializado
✅ Interface pronta para uso

Acesse: http://localhost:8501
```

## 📞 Suporte

Se ainda tiver problemas:

1. **Verifique os logs** no terminal onde executou o comando
2. **Teste os exemplos** em `exemplo_modelos_agno.py`
3. **Consulte a documentação** oficial do Agno
4. **Verifique as chaves de API** estão corretas

### **Comandos de Diagnóstico**
```bash
# Testar configuração completa
python exemplo_modelos_agno.py

# Verificar versões
pip list | grep -E "(streamlit|agno|openai|anthropic)"

# Testar Streamlit
streamlit hello
```

---

**🚀 Agora você pode usar a interface gráfica completa para criar agentes Agno de forma visual e intuitiva!**