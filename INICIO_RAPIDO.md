# 🚀 Início Rápido - Agno Agent Builder

## ⚡ Execução em 3 Passos

### **1. Instalar Dependências**
```bash
pip install streamlit agno openai anthropic google-generativeai
```

### **2. Configurar APIs (Opcional)**
```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar .env com suas chaves de API
# (ou configure na aba Settings da interface)
```

### **3. Executar Interface**
```bash
# Opção 1: Script completo (recomendado)
python start_agno_builder.py

# Opção 2: Interface simples
streamlit run agno_builder_simples.py
```

## 🌐 Acessar Interface

Abra no navegador: **http://localhost:8501**

## ⚙️ Configurar APIs na Interface

1. Acesse a aba **"Settings"**
2. Cole suas chaves de API nos campos
3. Clique em **"Salvar"** para cada provedor
4. Use **"Testar"** para verificar conexões

## 🔑 Obter Chaves de API

| Provedor | Link | Custo |
|----------|------|-------|
| **OpenAI** | https://platform.openai.com/api-keys | Pago |
| **Anthropic** | https://console.anthropic.com/ | Pago |
| **Google** | https://makersuite.google.com/app/apikey | Gratuito* |
| **OpenRouter** | https://openrouter.ai/keys | Varia** |

*Gratuito com limites, depois pago  
**Muitos modelos gratuitos disponíveis

## 🛠️ Usar a Interface

### **Aba Builder**
1. Selecione o **nível** do agente (1-5)
2. Configure **nome, papel e modelo**
3. Escolha **ferramentas** necessárias
4. Clique em **"Gerar Código"**
5. **Download** do código Python

### **Aba Settings**
1. Configure **chaves de API**
2. **Teste conexões** com provedores
3. Veja **status** das APIs na barra lateral

## 🎯 Níveis de Agentes

| Nível | Descrição | Recursos |
|-------|-----------|----------|
| **1** | Ferramentas & Instruções | Básico com tools |
| **2** | Conhecimento & RAG | Base de conhecimento |
| **3** | Memória & Raciocínio | Memória persistente |
| **4** | Times de Agentes | Múltiplos agentes |
| **5** | Workflows Agênticos | Fluxos complexos |

## 🔧 Solução de Problemas

### **Erro: "missing ScriptRunContext"**
✅ Use: `streamlit run agno_builder_simples.py`

### **Erro: "No module named 'agno'"**
✅ Execute: `pip install agno`

### **Erro: "API key not configured"**
✅ Configure na aba Settings ou arquivo .env

### **Interface não carrega**
✅ Tente: `python start_agno_builder.py`

## 📚 Recursos Úteis

- **Documentação Agno**: https://docs.agno.com
- **Modelos OpenRouter**: https://openrouter.ai/models
- **Exemplos**: Execute `python exemplo_modelos_agno.py`

## 🎉 Pronto!

Agora você pode criar agentes Agno visualmente! 🤖✨