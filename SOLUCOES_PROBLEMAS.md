# 🔧 Soluções para Problemas do Agno Builder

## ❌ Problema: "Descriptors cannot be created directly"

### **Causa**
Incompatibilidade entre versões do `protobuf` e `streamlit`.

### **✅ Soluções Implementadas**

#### **Solução 1: Correção Automática**
```bash
# Execute o script de correção
python fix_protobuf_issue.py
```

#### **Solução 2: Correção Manual**
```bash
# 1. Definir variável de ambiente
$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"  # Windows
export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python   # Linux/Mac

# 2. Downgrade do protobuf
pip install protobuf==3.20.3 --force-reinstall

# 3. Atualizar streamlit
pip install streamlit --upgrade
```

#### **Solução 3: Interface CLI (Sem Streamlit)**
```bash
# Use a versão CLI que não depende do Streamlit
python agno_builder_cli.py
```

## 🚀 Métodos de Execução (Em Ordem de Preferência)

### **1. Script Completo (Recomendado)**
```bash
python start_agno_builder.py
```
- ✅ Verifica todas as dependências
- ✅ Carrega configurações automaticamente
- ✅ Inicia interface automaticamente

### **2. Interface Simples com Settings**
```bash
# Definir variável de ambiente primeiro
$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"

# Executar interface
streamlit run agno_builder_simples.py --server.port 8503
```
- ✅ Interface web com aba Settings
- ✅ Configuração de APIs na interface
- ✅ Teste de conexões integrado

### **3. Interface CLI (Alternativa)**
```bash
python agno_builder_cli.py
```
- ✅ Não depende do Streamlit
- ✅ Interface de linha de comando
- ✅ Funciona mesmo com problemas de protobuf

### **4. Script de Inicialização**
```bash
streamlit run iniciar_agno_builder.py --server.port 8503
```
- ✅ Carrega .env automaticamente
- ✅ Verificações de dependências

## 🔑 Configuração de APIs

### **Método 1: Arquivo .env (Recomendado)**
```bash
# 1. Copiar arquivo de exemplo
cp .env.example .env

# 2. Editar .env com suas chaves
# OPENAI_API_KEY=sua_chave_openai
# ANTHROPIC_API_KEY=sua_chave_anthropic
# GOOGLE_API_KEY=sua_chave_google
# OPENROUTER_API_KEY=sua_chave_openrouter
```

### **Método 2: Interface Settings**
1. Acesse a aba **"Settings"** na interface web
2. Cole suas chaves nos campos
3. Clique em **"Salvar"** para cada provedor
4. Use **"Testar"** para verificar conexões

### **Método 3: Variáveis de Ambiente**
```bash
# Windows (PowerShell)
$env:OPENAI_API_KEY="sua_chave"
$env:ANTHROPIC_API_KEY="sua_chave"

# Linux/Mac (Bash)
export OPENAI_API_KEY="sua_chave"
export ANTHROPIC_API_KEY="sua_chave"
```

## 📦 Instalação de Dependências

### **Dependências Básicas**
```bash
pip install streamlit agno
```

### **Provedores de Modelos**
```bash
# Instale apenas os que for usar
pip install openai              # OpenAI
pip install anthropic           # Anthropic
pip install google-generativeai # Google Gemini
```

### **Instalação Completa**
```bash
pip install streamlit agno openai anthropic google-generativeai
```

## 🔍 Diagnóstico de Problemas

### **Verificar Instalações**
```bash
# Verificar Python
python --version

# Verificar Streamlit
streamlit --version

# Verificar Agno
python -c "import agno; print('✅ Agno OK')"

# Verificar protobuf
python -c "import google.protobuf; print('✅ Protobuf OK')"
```

### **Verificar APIs**
```bash
# Executar script de verificação
python load_env.py
```

### **Testar Interface**
```bash
# Testar Streamlit básico
streamlit hello

# Testar interface simples
streamlit run agno_builder_simples.py --server.port 8504
```

## 🆘 Problemas Comuns e Soluções

### **Erro: "Port already in use"**
```bash
# Use uma porta diferente
streamlit run agno_builder_simples.py --server.port 8504
```

### **Erro: "No module named 'agno'"**
```bash
# Instalar Agno
pip install agno
```

### **Erro: "API key not configured"**
- Configure na aba Settings da interface
- Ou use arquivo .env
- Ou defina variáveis de ambiente

### **Interface não carrega**
1. Verifique se está no diretório correto
2. Certifique-se que o ambiente virtual está ativo
3. Use a interface CLI como alternativa

### **Erro de importação do Streamlit**
```bash
# Reinstalar Streamlit
pip uninstall streamlit
pip install streamlit

# Ou usar versão específica
pip install streamlit==1.47.1
```

## 📊 Status das Soluções

| Método | Status | Observações |
|--------|--------|-------------|
| **start_agno_builder.py** | ✅ Funcionando | Recomendado |
| **agno_builder_simples.py** | ✅ Funcionando | Com correção protobuf |
| **agno_builder_cli.py** | ✅ Funcionando | Alternativa sem Streamlit |
| **iniciar_agno_builder.py** | ✅ Funcionando | Script básico |
| **agno_builder_interface.py** | ⚠️ Problemas | Pode ter issues de contexto |

## 🎯 Recomendação Final

**Para usuários iniciantes:**
```bash
python start_agno_builder.py
```

**Para usuários avançados:**
```bash
$env:PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION="python"
streamlit run agno_builder_simples.py --server.port 8503
```

**Para casos problemáticos:**
```bash
python agno_builder_cli.py
```

## 🔗 Links Úteis

- **Obter Chaves de API:**
  - [OpenAI](https://platform.openai.com/api-keys)
  - [Anthropic](https://console.anthropic.com/)
  - [Google](https://makersuite.google.com/app/apikey)
  - [OpenRouter](https://openrouter.ai/keys)

- **Documentação:**
  - [Agno Docs](https://docs.agno.com)
  - [Streamlit Docs](https://docs.streamlit.io)

---

**🎉 Com essas soluções, você deve conseguir executar a interface Agno Builder sem problemas!**