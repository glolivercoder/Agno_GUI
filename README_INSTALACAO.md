# Agno Framework - Instalação e Configuração

## 📋 Resumo

Este repositório contém a instalação e configuração do **Agno Framework**, um framework Python full-stack para construção de Sistemas Multi-Agentes com memória, conhecimento e raciocínio.

## 🚀 Instalação Realizada

### 1. Ambiente Virtual
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

### 2. Dependências Instaladas
```bash
# Instalação básica do Agno
pip install -e libs/agno/

# Modelos de IA
pip install "agno[openai]" "agno[anthropic]"

# Ferramentas e integrações
pip install "agno[tools]"

# Base de conhecimento
pip install "agno[knowledge]" pypdf

# Desenvolvimento
pip install "agno[dev]"
```

## 📁 Estrutura do Projeto

```
agno/
├── .venv/                          # Ambiente virtual
├── libs/agno/                      # Código fonte do Agno
├── cookbook/                       # Exemplos e tutoriais
├── scripts/                        # Scripts de desenvolvimento
├── memo.json                       # Resumo funcional da documentação
├── test_agno.py                    # Teste de instalação
├── exemplo_agno_basico.py          # Exemplos práticos
├── conhecimento_exemplo.txt        # Base de conhecimento de exemplo
├── agno_memory.db                  # Banco de dados de memória
└── README_INSTALACAO.md           # Este arquivo
```

## 🧪 Testes de Verificação

### Teste de Instalação
```bash
python test_agno.py
```

### Exemplos Práticos
```bash
python exemplo_agno_basico.py
```

## 🔑 Configuração de Chaves de API

Para usar os modelos de IA, configure as chaves de API:

### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="sua_chave_openai"
$env:ANTHROPIC_API_KEY="sua_chave_anthropic"
```

### Linux/Mac (Bash)
```bash
export OPENAI_API_KEY="sua_chave_openai"
export ANTHROPIC_API_KEY="sua_chave_anthropic"
```

### Arquivo .env
Crie um arquivo `.env` na raiz do projeto:
```env
OPENAI_API_KEY=sua_chave_openai
ANTHROPIC_API_KEY=sua_chave_anthropic
GROQ_API_KEY=sua_chave_groq
```

## 🤖 Exemplos de Uso

### 1. Agente Básico
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),
    instructions=["Você é um assistente útil."],
    markdown=True,
)

# Para testar (precisa da API key configurada)
# agent.print_response("Olá! Como você pode me ajudar?")
```

### 2. Agente com Ferramentas
```python
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools

agent = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),
    tools=[DuckDuckGoTools(), CalculatorTools()],
    instructions=["Use as ferramentas quando necessário."],
    show_tool_calls=True,
)
```

### 3. Time de Agentes
```python
from agno.team import Team

pesquisador = Agent(name="Pesquisador", tools=[DuckDuckGoTools()])
analista = Agent(name="Analista", tools=[CalculatorTools()])

team = Team(
    members=[pesquisador, analista],
    instructions=["Trabalhem juntos para resolver problemas."]
)
```

## 📚 Recursos do Agno

### 🎯 5 Níveis de Sistemas Agênticos
1. **Nível 1**: Agentes com ferramentas e instruções
2. **Nível 2**: Agentes com conhecimento e armazenamento  
3. **Nível 3**: Agentes com memória e raciocínio
4. **Nível 4**: Times de agentes que colaboram
5. **Nível 5**: Fluxos de trabalho agênticos com estado

### 🔧 Principais Características
- ⚡ **Performance**: Instantiação ~3μs, Memória ~6.5Kib
- 🤖 **23+ Modelos**: OpenAI, Anthropic, Google, AWS, Azure, etc.
- 🧠 **Raciocínio**: Modelos de raciocínio, ReasoningTools, chain-of-thought
- 🎭 **Multimodal**: Texto, imagem, áudio, vídeo
- 🔍 **RAG Agêntico**: 20+ bancos de dados vetoriais
- 💾 **Memória**: Persistente com múltiplos drivers
- 📊 **Monitoramento**: Tempo real em agno.com

### 🛠️ Ferramentas Disponíveis
- **Busca**: DuckDuckGo, Google, Brave, Exa, ArXiv
- **Web Scraping**: Firecrawl, Crawl4AI, Newspaper4k
- **Bancos de Dados**: PostgreSQL, MongoDB, SQLite, Redis
- **Social**: Email, Slack, Discord, WhatsApp, Twitter
- **Desenvolvimento**: GitHub, Docker, Python, Shell
- **Multimodal**: DALL-E, ElevenLabs, Replicate

## 📖 Documentação e Recursos

- **Documentação**: https://docs.agno.com
- **Exemplos**: https://docs.agno.com/examples
- **GitHub**: https://github.com/agno-agi/agno
- **Discord**: https://discord.gg/4MtYHHrgA8
- **Fórum**: https://community.agno.com

## 🎯 Próximos Passos

1. **Configure as chaves de API** para testar os modelos
2. **Execute os exemplos** em `exemplo_agno_basico.py`
3. **Explore o cookbook** em `cookbook/` para mais exemplos
4. **Consulte a documentação** para funcionalidades avançadas
5. **Monitore seus agentes** em https://app.agno.com

## 📋 Resumo Funcional

O arquivo `memo.json` contém um resumo completo e estruturado de todas as funcionalidades, modelos suportados, ferramentas disponíveis e casos de uso do Agno Framework.

## ✅ Status da Instalação

- ✅ Ambiente virtual criado
- ✅ Agno Framework instalado
- ✅ Dependências principais instaladas
- ✅ Testes de verificação passando
- ✅ Exemplos funcionando
- ✅ Documentação organizada

**🎉 Agno Framework está pronto para uso!**