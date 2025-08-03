# Manual Completo do Agno Framework 🤖

## Índice
1. [Introdução](#introdução)
2. [Instalação e Configuração](#instalação-e-configuração)
3. [Conceitos Fundamentais](#conceitos-fundamentais)
4. [Interfaces Visuais](#interfaces-visuais)
5. [Criando Agentes](#criando-agentes)
6. [Trabalhando com Ferramentas](#trabalhando-com-ferramentas)
7. [Times de Agentes](#times-de-agentes)
8. [Workflows Agênticos](#workflows-agênticos)
9. [Sistema de Conhecimento (RAG)](#sistema-de-conhecimento-rag)
10. [Sistema de Memória](#sistema-de-memória)
11. [Exemplos Práticos](#exemplos-práticos)
12. [Monitoramento e Observabilidade](#monitoramento-e-observabilidade)
13. [Melhores Práticas](#melhores-práticas)
14. [Recursos e Comunidade](#recursos-e-comunidade)

---

## Introdução

O **Agno** é um framework Python full-stack para construção de Sistemas Multi-Agentes com memória, conhecimento e raciocínio. Ele permite criar desde agentes simples até sistemas complexos de múltiplos agentes que colaboram entre si.

### 🎯 Os 5 Níveis de Sistemas Agênticos

O Agno permite construir sistemas agênticos em 5 níveis de complexidade:

1. **Nível 1**: Agentes com ferramentas e instruções
2. **Nível 2**: Agentes com conhecimento e armazenamento  
3. **Nível 3**: Agentes com memória e raciocínio
4. **Nível 4**: Times de agentes que colaboram
5. **Nível 5**: Fluxos de trabalho agênticos com estado

### ⚡ Características Principais

- **Performance Excepcional**: Instantiação ~3μs, Memória ~6.5Kib
- **23+ Modelos Suportados**: OpenAI, Anthropic, Google, AWS, Azure, etc.
- **Multimodal Nativo**: Texto, imagem, áudio, vídeo
- **RAG Agêntico**: 20+ bancos de dados vetoriais
- **Memória Persistente**: Sistema avançado de memória
- **Monitoramento**: Tempo real em agno.com

---

## Instalação e Configuração

### 📦 Instalação Básica

```bash
# Instalação básica
pip install -U agno

# Com suporte a modelos específicos
pip install "agno[openai]" "agno[anthropic]"

# Com todas as ferramentas
pip install "agno[tools]"

# Para desenvolvimento
pip install "agno[dev]"
```

### 🔑 Configuração de Chaves de API

#### Windows (PowerShell)
```powershell
$env:OPENAI_API_KEY="sua_chave_openai"
$env:ANTHROPIC_API_KEY="sua_chave_anthropic"
$env:GOOGLE_API_KEY="sua_chave_google"
```

#### Linux/Mac (Bash)
```bash
export OPENAI_API_KEY="sua_chave_openai"
export ANTHROPIC_API_KEY="sua_chave_anthropic"
export GOOGLE_API_KEY="sua_chave_google"
```

#### Arquivo .env
```env
OPENAI_API_KEY=sua_chave_openai
ANTHROPIC_API_KEY=sua_chave_anthropic
GOOGLE_API_KEY=sua_chave_google
GROQ_API_KEY=sua_chave_groq
```

---

## Conceitos Fundamentais

### 🤖 Agentes
Agentes são a unidade atômica de trabalho no Agno. Cada agente tem:
- **Modelo de IA**: O cérebro do agente
- **Instruções**: Como o agente deve se comportar
- **Ferramentas**: O que o agente pode fazer
- **Conhecimento**: Informações que o agente pode acessar
- **Memória**: Capacidade de lembrar conversas anteriores

### 👥 Times (Teams)
Times são grupos de agentes que trabalham juntos:
- **Collaborate**: Agentes colaboram em tarefas
- **Coordinate**: Coordenação entre agentes
- **Route**: Roteamento inteligente de tarefas

### 🔄 Workflows
Fluxos de trabalho estruturados com estado e determinismo:
- Sequencial, paralelo, condicional
- Controle de estado
- Recuperação de falhas

---

## Interfaces Visuais

### 🎮 Playground do Agno

O Agno oferece uma interface web interativa para testar e desenvolver agentes:

```python
from agno.playground import Playground
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Criar agente
agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    instructions=["Você é um assistente útil."]
)

# Iniciar playground
playground = Playground(agents=[agent])
playground.serve(port=8000)
```

Acesse: `http://localhost:8000`

### 📊 Interface de Monitoramento

Monitore seus agentes em tempo real:
- Acesse: https://app.agno.com
- Visualize métricas de performance
- Analise conversas e decisões
- Monitore custos de API

### 🔧 Interface de Desenvolvimento

Use IDEs como VSCode ou Cursor com suporte completo:
- Autocomplete inteligente
- Debugging integrado
- Documentação inline
- Exemplos contextuais

---

## Criando Agentes

### 🚀 Agente Básico (Nível 1)

```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Agente básico com personalidade
agente_basico = Agent(
    model=OpenAIChat(id="gpt-4"),
    instructions=[
        "Você é um assistente brasileiro amigável.",
        "Use emojis quando apropriado.",
        "Seja conciso e claro nas respostas."
    ],
    markdown=True,
)

# Testar o agente
agente_basico.print_response("Olá! Como você pode me ajudar?")
```

### 🛠️ Agente com Ferramentas (Nível 1)

```python
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools

agente_pesquisador = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        DuckDuckGoTools(),
        CalculatorTools()
    ],
    instructions=[
        "Você é um pesquisador especializado.",
        "Use as ferramentas para buscar informações atuais.",
        "Sempre cite suas fontes.",
        "Faça cálculos quando necessário."
    ],
    show_tool_calls=True,
    markdown=True,
)

# Exemplo de uso
agente_pesquisador.print_response(
    "Pesquise sobre o PIB do Brasil em 2024 e calcule a diferença percentual com 2023"
)
```

### 📚 Agente com Conhecimento (Nível 2)

```python
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.chroma import ChromaDb

# Criar base de conhecimento
knowledge_base = TextKnowledgeBase(
    path="documentos/",
    vector_db=ChromaDb(
        collection="minha_empresa",
        path="vectordb/"
    )
)

agente_especialista = Agent(
    model=OpenAIChat(id="gpt-4"),
    knowledge=knowledge_base,
    instructions=[
        "Você é um especialista da empresa.",
        "Use apenas informações da base de conhecimento.",
        "Sempre referencie a fonte das informações.",
        "Se não souber, diga que não está na base de conhecimento."
    ],
    markdown=True,
)

# Exemplo de uso
agente_especialista.print_response(
    "Quais são as políticas de RH da nossa empresa?"
)
```

### 🧠 Agente com Memória (Nível 3)

```python
from agno.memory import Memory
from agno.storage.sqlite import SqliteStorage

# Configurar armazenamento
storage = SqliteStorage(
    table_name="conversas_agente",
    db_file="memoria_agente.db"
)

agente_com_memoria = Agent(
    model=OpenAIChat(id="gpt-4"),
    storage=storage,
    add_history_to_messages=True,
    instructions=[
        "Você é um assistente pessoal com memória.",
        "Lembre-se das conversas anteriores.",
        "Use o contexto histórico para personalizar respostas.",
        "Mantenha um tom consistente ao longo das sessões."
    ],
    markdown=True,
)

# Primeira conversa
agente_com_memoria.print_response("Meu nome é João e trabalho com marketing.")

# Segunda conversa (em outra sessão)
agente_com_memoria.print_response("Você lembra qual é minha área de trabalho?")
```

### 🎯 Agente com Raciocínio

```python
from agno.tools.reasoning import ReasoningTools

agente_raciocinante = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        ReasoningTools(add_instructions=True),
        DuckDuckGoTools(),
        CalculatorTools()
    ],
    instructions=[
        "Você é um analista que pensa antes de agir.",
        "Use o raciocínio estruturado para resolver problemas.",
        "Mostre seu processo de pensamento.",
        "Valide suas conclusões com dados."
    ],
    show_tool_calls=True,
    markdown=True,
)

# Exemplo complexo
agente_raciocinante.print_response(
    "Analise se vale a pena investir em ações da Tesla considerando "
    "os dados financeiros atuais e tendências do mercado de carros elétricos",
    show_full_reasoning=True
)
```

---

## Trabalhando com Ferramentas

### 🔍 Ferramentas de Busca

```python
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.googlesearch import GoogleSearchTools
from agno.tools.exa import ExaTools

agente_busca = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        DuckDuckGoTools(),
        GoogleSearchTools(),  # Requer API key
        ExaTools()  # Requer API key
    ],
    instructions=["Use múltiplas fontes para validar informações."]
)
```

### 🌐 Ferramentas Web

```python
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.newspaper4k import Newspaper4kTools

agente_web = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        FirecrawlTools(),  # Web scraping avançado
        Newspaper4kTools()  # Extração de artigos
    ],
    instructions=["Extraia informações relevantes de websites."]
)
```

### 💰 Ferramentas Financeiras

```python
from agno.tools.yfinance import YFinanceTools
from agno.tools.openbb import OpenBBTools

agente_financeiro = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True
        ),
        OpenBBTools()  # Dados financeiros avançados
    ],
    instructions=[
        "Forneça análises financeiras detalhadas.",
        "Use tabelas para apresentar dados.",
        "Inclua recomendações baseadas em dados."
    ]
)
```

### 📊 Ferramentas de Dados

```python
from agno.tools.pandas import PandasTools
from agno.tools.sql import SqlTools

agente_dados = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        PandasTools(),
        SqlTools(
            db_url="postgresql://user:pass@localhost/db"
        )
    ],
    instructions=[
        "Analise dados de forma estruturada.",
        "Crie visualizações quando apropriado.",
        "Explique insights encontrados."
    ]
)
```

### 🎨 Ferramentas Multimodais

```python
from agno.tools.dalle import DalleTools
from agno.tools.elevenlabs import ElevenLabsTools

agente_criativo = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        DalleTools(),  # Geração de imagens
        ElevenLabsTools()  # Síntese de voz
    ],
    instructions=[
        "Crie conteúdo visual e auditivo.",
        "Descreva detalhadamente as criações.",
        "Adapte o estilo ao contexto solicitado."
    ]
)
```

### 🔧 Criando Ferramentas Personalizadas

```python
from agno.tools import Tool
from typing import Optional

def consultar_api_interna(query: str) -> str:
    """Consulta API interna da empresa"""
    # Implementação da consulta
    return f"Resultado para: {query}"

# Registrar como ferramenta
ferramenta_personalizada = Tool(
    name="consultar_api_interna",
    description="Consulta dados internos da empresa",
    function=consultar_api_interna
)

agente_personalizado = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[ferramenta_personalizada],
    instructions=["Use a API interna para consultas específicas."]
)
```

---

## Times de Agentes

### 👥 Time Colaborativo (Nível 4)

```python
from agno.team import Team

# Agente Pesquisador
pesquisador = Agent(
    name="Pesquisador",
    role="Busca informações na web",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Pesquise informações atuais e relevantes.",
        "Sempre inclua fontes confiáveis.",
        "Foque em dados factuais."
    ]
)

# Agente Analista
analista = Agent(
    name="Analista",
    role="Analisa dados e faz cálculos",
    model=OpenAIChat(id="gpt-4"),
    tools=[CalculatorTools(), PandasTools()],
    instructions=[
        "Analise dados de forma estruturada.",
        "Faça cálculos precisos.",
        "Apresente insights claros."
    ]
)

# Agente Editor
editor = Agent(
    name="Editor",
    role="Compila e formata relatórios",
    model=OpenAIChat(id="gpt-4"),
    instructions=[
        "Compile informações de outros agentes.",
        "Crie relatórios bem estruturados.",
        "Use formatação markdown."
    ]
)

# Criar time
time_pesquisa = Team(
    members=[pesquisador, analista, editor],
    model=OpenAIChat(id="gpt-4"),
    mode="collaborate",
    instructions=[
        "Trabalhem juntos para criar relatórios completos.",
        "Cada agente deve contribuir com sua especialidade.",
        "O editor deve compilar o trabalho final."
    ],
    show_tool_calls=True,
    markdown=True
)

# Usar o time
time_pesquisa.print_response(
    "Criem um relatório sobre o mercado de carros elétricos no Brasil, "
    "incluindo dados de vendas, principais players e projeções futuras."
)
```

### 🎯 Time com Coordenação

```python
time_coordenado = Team(
    members=[pesquisador, analista, editor],
    mode="coordinate",  # Coordenação inteligente
    model=OpenAIChat(id="gpt-4"),
    success_criteria="Relatório completo com dados, análise e conclusões",
    instructions=[
        "Coordenem o trabalho de forma eficiente.",
        "Evitem duplicação de esforços.",
        "Garantam qualidade e completude."
    ]
)
```

### 🔀 Time com Roteamento

```python
# Agente Especialista em Tecnologia
tech_expert = Agent(
    name="Especialista Tech",
    role="Especialista em tecnologia",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=["Foque em aspectos técnicos e inovações."]
)

# Agente Especialista em Negócios
business_expert = Agent(
    name="Especialista Negócios",
    role="Especialista em negócios",
    model=OpenAIChat(id="gpt-4"),
    tools=[YFinanceTools()],
    instructions=["Foque em aspectos financeiros e de mercado."]
)

time_roteamento = Team(
    members=[tech_expert, business_expert],
    mode="route",  # Roteamento inteligente
    model=OpenAIChat(id="gpt-4"),
    instructions=[
        "Roteie perguntas para o especialista apropriado.",
        "Perguntas técnicas vão para o especialista tech.",
        "Perguntas de negócios vão para o especialista business."
    ]
)

# Teste de roteamento
time_roteamento.print_response("Qual é a arquitetura do ChatGPT?")  # → Tech Expert
time_roteamento.print_response("Como está o mercado de ações da OpenAI?")  # → Business Expert
```

---

## Workflows Agênticos

### 🔄 Workflow Sequencial (Nível 5)

```python
from agno.workflow import Workflow
from agno.workflow.task import Task

# Definir tarefas
tarefa_pesquisa = Task(
    name="pesquisa",
    agent=pesquisador,
    description="Pesquisar informações sobre o tópico"
)

tarefa_analise = Task(
    name="analise",
    agent=analista,
    description="Analisar dados coletados",
    depends_on=["pesquisa"]  # Depende da pesquisa
)

tarefa_relatorio = Task(
    name="relatorio",
    agent=editor,
    description="Criar relatório final",
    depends_on=["pesquisa", "analise"]  # Depende de ambas
)

# Criar workflow
workflow_pesquisa = Workflow(
    name="Workflow de Pesquisa",
    tasks=[tarefa_pesquisa, tarefa_analise, tarefa_relatorio]
)

# Executar workflow
resultado = workflow_pesquisa.run(
    input_data={"topico": "Inteligência Artificial no Brasil"}
)
```

### 🔀 Workflow Condicional

```python
from agno.workflow.condition import Condition

# Condição para determinar próximo passo
def verificar_qualidade_dados(context):
    return context.get("qualidade_dados", 0) > 0.8

tarefa_validacao = Task(
    name="validacao",
    agent=analista,
    description="Validar qualidade dos dados"
)

tarefa_coleta_adicional = Task(
    name="coleta_adicional",
    agent=pesquisador,
    description="Coletar dados adicionais",
    condition=Condition(
        check=lambda ctx: not verificar_qualidade_dados(ctx)
    )
)

workflow_condicional = Workflow(
    name="Workflow com Validação",
    tasks=[tarefa_pesquisa, tarefa_validacao, tarefa_coleta_adicional, tarefa_analise]
)
```

### ⚡ Workflow Paralelo

```python
# Tarefas que podem executar em paralelo
tarefa_pesquisa_web = Task(
    name="pesquisa_web",
    agent=pesquisador,
    description="Pesquisar na web"
)

tarefa_pesquisa_papers = Task(
    name="pesquisa_papers",
    agent=Agent(
        model=OpenAIChat(id="gpt-4"),
        tools=[ArxivTools()],
        instructions=["Pesquise papers acadêmicos."]
    ),
    description="Pesquisar papers acadêmicos"
)

# Executam em paralelo
tarefa_compilacao = Task(
    name="compilacao",
    agent=editor,
    description="Compilar todas as pesquisas",
    depends_on=["pesquisa_web", "pesquisa_papers"]
)

workflow_paralelo = Workflow(
    name="Pesquisa Paralela",
    tasks=[tarefa_pesquisa_web, tarefa_pesquisa_papers, tarefa_compilacao],
    parallel=True  # Permite execução paralela
)
```

---

## Sistema de Conhecimento (RAG)

### 📚 Base de Conhecimento Básica

```python
from agno.knowledge.text import TextKnowledgeBase
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.knowledge.website import WebsiteKnowledgeBase

# Base de conhecimento de texto
kb_texto = TextKnowledgeBase(
    path="documentos/",
    formats=[".txt", ".md", ".json"]
)

# Base de conhecimento PDF
kb_pdf = PDFKnowledgeBase(
    path="pdfs/",
    chunk_size=1000,
    chunk_overlap=200
)

# Base de conhecimento de websites
kb_web = WebsiteKnowledgeBase(
    urls=[
        "https://docs.agno.com",
        "https://python.org/docs"
    ]
)

# Combinar bases de conhecimento
agente_rag = Agent(
    model=OpenAIChat(id="gpt-4"),
    knowledge=[kb_texto, kb_pdf, kb_web],
    instructions=[
        "Use as bases de conhecimento para responder perguntas.",
        "Sempre cite a fonte das informações.",
        "Se não encontrar informação relevante, diga claramente."
    ]
)
```

### 🔍 RAG Avançado com Filtros

```python
from agno.knowledge.document import Document
from agno.vectordb.pgvector import PgVector

# Configurar banco vetorial
vector_db = PgVector(
    collection="empresa_docs",
    db_url="postgresql://user:pass@localhost/vectordb"
)

# Base de conhecimento com metadados
kb_avancada = TextKnowledgeBase(
    path="documentos_empresa/",
    vector_db=vector_db,
    chunk_size=500,
    chunk_overlap=100,
    # Adicionar metadados aos documentos
    metadata_func=lambda doc: {
        "departamento": doc.path.split("/")[1],
        "tipo": doc.path.split(".")[-1],
        "data_criacao": doc.created_at
    }
)

# Agente com busca filtrada
agente_rag_filtrado = Agent(
    model=OpenAIChat(id="gpt-4"),
    knowledge=kb_avancada,
    instructions=[
        "Use filtros de metadados quando apropriado.",
        "Priorize documentos mais recentes.",
        "Considere o departamento relevante para a pergunta."
    ]
)

# Busca com filtros
agente_rag_filtrado.print_response(
    "Quais são as políticas de RH mais recentes?",
    knowledge_filters={"departamento": "rh"}
)
```

### 🧠 RAG com Recuperação Híbrida

```python
from agno.knowledge.retriever import HybridRetriever

# Recuperador híbrido (palavra-chave + vetorial)
hybrid_retriever = HybridRetriever(
    vector_weight=0.7,  # 70% busca vetorial
    keyword_weight=0.3,  # 30% busca por palavra-chave
    top_k=10
)

kb_hibrida = TextKnowledgeBase(
    path="base_conhecimento/",
    retriever=hybrid_retriever
)

agente_rag_hibrido = Agent(
    model=OpenAIChat(id="gpt-4"),
    knowledge=kb_hibrida,
    instructions=[
        "Use busca híbrida para melhor precisão.",
        "Combine relevância semântica com correspondência exata.",
        "Explique como encontrou as informações."
    ]
)
```

---

## Sistema de Memória

### 🧠 Memória de Sessão

```python
from agno.memory import Memory
from agno.storage.sqlite import SqliteStorage

# Configurar memória de sessão
session_storage = SqliteStorage(
    table_name="sessoes_usuario",
    db_file="memoria_sessoes.db"
)

agente_sessao = Agent(
    model=OpenAIChat(id="gpt-4"),
    storage=session_storage,
    session_id="usuario_123",  # ID único do usuário
    add_history_to_messages=True,
    instructions=[
        "Mantenha contexto da conversa atual.",
        "Lembre-se de preferências mencionadas.",
        "Adapte respostas ao histórico da sessão."
    ]
)
```

### 💾 Memória de Longo Prazo

```python
from agno.memory.long_term import LongTermMemory

# Memória de longo prazo
long_term_memory = LongTermMemory(
    storage=SqliteStorage(
        table_name="memoria_longo_prazo",
        db_file="memoria_persistente.db"
    ),
    summarize_after=10,  # Resumir após 10 mensagens
    max_memories=1000    # Máximo de memórias
)

agente_memoria_longa = Agent(
    model=OpenAIChat(id="gpt-4"),
    memory=long_term_memory,
    user_id="usuario_123",
    instructions=[
        "Use memória de longo prazo para personalização.",
        "Lembre-se de informações importantes do usuário.",
        "Construa relacionamento ao longo do tempo."
    ]
)

# Primeira conversa
agente_memoria_longa.print_response(
    "Meu nome é Maria, sou engenheira de software e gosto de Python."
)

# Semanas depois...
agente_memoria_longa.print_response(
    "Você lembra qual linguagem de programação eu prefiro?"
)
```

### 🤝 Memória Compartilhada

```python
from agno.memory.shared import SharedMemory

# Memória compartilhada entre agentes
shared_memory = SharedMemory(
    storage=SqliteStorage(
        table_name="memoria_compartilhada",
        db_file="memoria_time.db"
    ),
    team_id="time_vendas"
)

# Agente de vendas
agente_vendas = Agent(
    name="Vendedor",
    model=OpenAIChat(id="gpt-4"),
    memory=shared_memory,
    instructions=["Compartilhe informações de clientes com o time."]
)

# Agente de suporte
agente_suporte = Agent(
    name="Suporte",
    model=OpenAIChat(id="gpt-4"),
    memory=shared_memory,
    instructions=["Use informações compartilhadas para melhor atendimento."]
)
```

---

## Exemplos Práticos

### 🏢 Assistente Empresarial Completo

```python
# Assistente empresarial com todas as funcionalidades
assistente_empresarial = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[
        DuckDuckGoTools(),
        CalculatorTools(),
        EmailTools(),
        GoogleSheetsTools(),
        SlackTools()
    ],
    knowledge=TextKnowledgeBase(path="documentos_empresa/"),
    storage=SqliteStorage(
        table_name="assistente_sessoes",
        db_file="assistente.db"
    ),
    instructions=[
        "Você é um assistente empresarial completo.",
        "Use ferramentas para executar tarefas práticas.",
        "Consulte a base de conhecimento para políticas internas.",
        "Mantenha histórico de interações.",
        "Seja proativo em sugerir melhorias."
    ],
    markdown=True
)

# Exemplos de uso
assistente_empresarial.print_response(
    "Preciso enviar um relatório de vendas por email para a diretoria. "
    "Busque os dados mais recentes e prepare o relatório."
)
```

### 📊 Sistema de Análise Financeira

```python
# Time especializado em análise financeira
analista_mercado = Agent(
    name="Analista de Mercado",
    model=OpenAIChat(id="gpt-4"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True
        ),
        DuckDuckGoTools()
    ],
    instructions=[
        "Analise dados de mercado e notícias financeiras.",
        "Foque em tendências e indicadores técnicos.",
        "Sempre inclua fontes e datas."
    ]
)

analista_fundamentalista = Agent(
    name="Analista Fundamentalista",
    model=OpenAIChat(id="gpt-4"),
    tools=[
        YFinanceTools(
            company_info=True,
            financials=True,
            balance_sheet=True
        ),
        CalculatorTools()
    ],
    instructions=[
        "Analise fundamentos das empresas.",
        "Calcule métricas financeiras importantes.",
        "Avalie saúde financeira e potencial de crescimento."
    ]
)

relator_financeiro = Agent(
    name="Relator Financeiro",
    model=OpenAIChat(id="gpt-4"),
    instructions=[
        "Compile análises em relatórios estruturados.",
        "Use tabelas e gráficos quando apropriado.",
        "Inclua recomendações claras de investimento."
    ]
)

time_financeiro = Team(
    members=[analista_mercado, analista_fundamentalista, relator_financeiro],
    model=OpenAIChat(id="gpt-4"),
    mode="collaborate",
    instructions=[
        "Trabalhem juntos para análises financeiras completas.",
        "Combinem análise técnica e fundamentalista.",
        "Produzam relatórios de investimento profissionais."
    ]
)

# Análise completa
time_financeiro.print_response(
    "Façam uma análise completa das ações da Petrobras (PETR4), "
    "incluindo análise técnica, fundamentalista e recomendação de investimento."
)
```

### 🎓 Sistema Educacional Inteligente

```python
# Professor virtual com especialidades
professor_matematica = Agent(
    name="Professor de Matemática",
    model=OpenAIChat(id="gpt-4"),
    tools=[CalculatorTools()],
    instructions=[
        "Ensine matemática de forma didática.",
        "Use exemplos práticos e exercícios.",
        "Adapte explicações ao nível do aluno.",
        "Sempre verifique se o aluno entendeu."
    ]
)

professor_ciencias = Agent(
    name="Professor de Ciências",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools(), WikipediaTools()],
    knowledge=TextKnowledgeBase(path="livros_ciencias/"),
    instructions=[
        "Ensine ciências com base em evidências.",
        "Use experimentos e exemplos do cotidiano.",
        "Consulte fontes confiáveis para informações atuais."
    ]
)

tutor_personalizado = Agent(
    name="Tutor Personalizado",
    model=OpenAIChat(id="gpt-4"),
    storage=SqliteStorage(
        table_name="progresso_alunos",
        db_file="educacao.db"
    ),
    instructions=[
        "Acompanhe o progresso individual de cada aluno.",
        "Identifique dificuldades e pontos fortes.",
        "Sugira planos de estudo personalizados.",
        "Motive e encoraje o aprendizado."
    ]
)

sistema_educacional = Team(
    members=[professor_matematica, professor_ciencias, tutor_personalizado],
    model=OpenAIChat(id="gpt-4"),
    mode="coordinate",
    instructions=[
        "Trabalhem juntos para educação completa.",
        "Adaptem métodos ao perfil do aluno.",
        "Mantenham registro de progresso.",
        "Promovam aprendizado interdisciplinar."
    ]
)
```

### 🛒 E-commerce Inteligente

```python
# Sistema completo de e-commerce
assistente_vendas = Agent(
    name="Assistente de Vendas",
    model=OpenAIChat(id="gpt-4"),
    knowledge=TextKnowledgeBase(path="catalogo_produtos/"),
    storage=SqliteStorage(
        table_name="interacoes_clientes",
        db_file="ecommerce.db"
    ),
    instructions=[
        "Ajude clientes a encontrar produtos ideais.",
        "Use histórico de compras para recomendações.",
        "Seja persuasivo mas honesto.",
        "Foque na satisfação do cliente."
    ]
)

suporte_tecnico = Agent(
    name="Suporte Técnico",
    model=OpenAIChat(id="gpt-4"),
    knowledge=TextKnowledgeBase(path="manuais_produtos/"),
    tools=[EmailTools()],
    instructions=[
        "Resolva problemas técnicos dos clientes.",
        "Use manuais e documentação técnica.",
        "Escale para humanos quando necessário.",
        "Documente soluções para casos futuros."
    ]
)

analista_comportamento = Agent(
    name="Analista de Comportamento",
    model=OpenAIChat(id="gpt-4"),
    tools=[PandasTools(), CalculatorTools()],
    instructions=[
        "Analise padrões de comportamento dos clientes.",
        "Identifique oportunidades de upsell/cross-sell.",
        "Sugira melhorias na experiência do usuário.",
        "Monitore métricas de satisfação."
    ]
)

sistema_ecommerce = Team(
    members=[assistente_vendas, suporte_tecnico, analista_comportamento],
    model=OpenAIChat(id="gpt-4"),
    mode="route",
    instructions=[
        "Roteiem clientes para o especialista apropriado.",
        "Vendas para assistente de vendas.",
        "Problemas técnicos para suporte.",
        "Análises para o analista de comportamento."
    ]
)
```

---

## Monitoramento e Observabilidade

### 📊 Monitoramento na Plataforma Agno

```python
# Configurar monitoramento automático
import os
os.environ["AGNO_API_KEY"] = "sua_chave_agno"

agente_monitorado = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    # Monitoramento automático habilitado
    monitoring=True,
    instructions=["Você será monitorado na plataforma Agno."]
)

# Todas as interações serão visíveis em https://app.agno.com
```

### 📈 Métricas Personalizadas

```python
from agno.monitoring import AgnoMonitoring

# Configurar métricas personalizadas
monitoring = AgnoMonitoring(
    api_key="sua_chave_agno",
    project_name="meu_projeto",
    custom_metrics=[
        "tempo_resposta",
        "satisfacao_usuario",
        "custo_por_interacao"
    ]
)

agente_com_metricas = Agent(
    model=OpenAIChat(id="gpt-4"),
    monitoring=monitoring,
    instructions=["Agente com métricas personalizadas."]
)

# Registrar métricas personalizadas
def callback_metricas(response, metadata):
    monitoring.log_metric("tempo_resposta", metadata.get("duration"))
    monitoring.log_metric("custo_por_interacao", metadata.get("cost"))

agente_com_metricas.add_callback(callback_metricas)
```

### 🔍 Debug e Logging

```python
import logging
from agno.logging import setup_agno_logging

# Configurar logging detalhado
setup_agno_logging(level=logging.DEBUG)

agente_debug = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    debug=True,  # Modo debug habilitado
    show_tool_calls=True,
    instructions=["Agente com logging detalhado."]
)

# Logs detalhados serão exibidos no console
```

---

## Melhores Práticas

### ⚡ Performance

```python
# ✅ Boas práticas de performance

# 1. Agentes com escopo estreito
agente_especializado = Agent(
    model=OpenAIChat(id="gpt-3.5-turbo"),  # Modelo mais rápido para tarefas simples
    tools=[CalculatorTools()],  # Apenas ferramentas necessárias
    instructions=["Foque apenas em cálculos matemáticos."]
)

# 2. Cache de resultados
from agno.cache import RedisCache

cache = RedisCache(host="localhost", port=6379)

agente_com_cache = Agent(
    model=OpenAIChat(id="gpt-4"),
    cache=cache,
    cache_ttl=3600,  # Cache por 1 hora
    instructions=["Use cache para respostas similares."]
)

# 3. Processamento paralelo
import asyncio

async def processar_multiplas_consultas():
    agentes = [
        Agent(model=OpenAIChat(id="gpt-3.5-turbo"))
        for _ in range(5)
    ]
    
    consultas = [
        "Pergunta 1", "Pergunta 2", "Pergunta 3",
        "Pergunta 4", "Pergunta 5"
    ]
    
    # Processar em paralelo
    resultados = await asyncio.gather(*[
        agente.arun(consulta)
        for agente, consulta in zip(agentes, consultas)
    ])
    
    return resultados
```

### 🛡️ Segurança e Confiabilidade

```python
# ✅ Práticas de segurança

# 1. Validação de entrada
def validar_entrada(texto: str) -> bool:
    """Valida entrada do usuário"""
    palavras_proibidas = ["hack", "exploit", "malware"]
    return not any(palavra in texto.lower() for palavra in palavras_proibidas)

agente_seguro = Agent(
    model=OpenAIChat(id="gpt-4"),
    instructions=[
        "Nunca execute comandos perigosos.",
        "Valide todas as entradas do usuário.",
        "Rejeite solicitações maliciosas."
    ]
)

# 2. Tratamento de erros
from agno.exceptions import AgnoException

def agente_com_tratamento_erro():
    try:
        agente = Agent(model=OpenAIChat(id="gpt-4"))
        resposta = agente.run("Sua pergunta aqui")
        return resposta
    except AgnoException as e:
        print(f"Erro do Agno: {e}")
        return "Desculpe, ocorreu um erro. Tente novamente."
    except Exception as e:
        print(f"Erro geral: {e}")
        return "Erro inesperado. Contate o suporte."

# 3. Confirmação humana para ações críticas
agente_critico = Agent(
    model=OpenAIChat(id="gpt-4"),
    tools=[EmailTools(), SlackTools()],
    instructions=[
        "Para ações críticas, sempre peça confirmação humana.",
        "Nunca execute ações irreversíveis sem aprovação.",
        "Documente todas as ações executadas."
    ]
)
```

### 📝 Documentação e Manutenção

```python
# ✅ Práticas de documentação

class AgenteProdução:
    """
    Agente de produção com documentação completa.
    
    Funcionalidades:
    - Pesquisa web
    - Cálculos matemáticos
    - Geração de relatórios
    
    Limitações:
    - Não executa comandos do sistema
    - Não acessa dados sensíveis
    
    Uso:
    >>> agente = AgenteProdução()
    >>> resposta = agente.processar("Sua pergunta")
    """
    
    def __init__(self):
        self.agente = Agent(
            model=OpenAIChat(id="gpt-4"),
            tools=[DuckDuckGoTools(), CalculatorTools()],
            instructions=[
                "Você é um assistente de produção.",
                "Sempre documente suas ações.",
                "Mantenha logs detalhados."
            ]
        )
    
    def processar(self, pergunta: str) -> str:
        """
        Processa uma pergunta e retorna resposta.
        
        Args:
            pergunta: Pergunta do usuário
            
        Returns:
            Resposta processada pelo agente
        """
        return self.agente.run(pergunta)
```

### 🧪 Testes

```python
# ✅ Testes para agentes
import pytest
from unittest.mock import Mock

def test_agente_basico():
    """Testa funcionalidade básica do agente"""
    agente = Agent(
        model=OpenAIChat(id="gpt-3.5-turbo"),
        instructions=["Responda sempre com 'Olá!'"]
    )
    
    # Mock da resposta do modelo
    agente.model.run = Mock(return_value="Olá!")
    
    resposta = agente.run("Qualquer pergunta")
    assert resposta == "Olá!"

def test_agente_com_ferramentas():
    """Testa agente com ferramentas"""
    agente = Agent(
        model=OpenAIChat(id="gpt-3.5-turbo"),
        tools=[CalculatorTools()]
    )
    
    # Teste de cálculo
    resposta = agente.run("Quanto é 2 + 2?")
    assert "4" in resposta

def test_time_agentes():
    """Testa time de agentes"""
    agente1 = Agent(name="Agente1", model=OpenAIChat(id="gpt-3.5-turbo"))
    agente2 = Agent(name="Agente2", model=OpenAIChat(id="gpt-3.5-turbo"))
    
    time = Team(members=[agente1, agente2])
    
    assert len(time.members) == 2
    assert time.members[0].name == "Agente1"
```

---

## Interface Gráfica para Criação de Agentes

### 🎨 Proposta de Interface Visual por Níveis

Baseado na análise da documentação do Agno, identifiquei que atualmente o framework possui:

#### ✅ **Interfaces Existentes**
- **Playground Web**: Interface para testar agentes criados
- **Monitoramento**: Dashboard em agno.com para observabilidade
- **IDE Integration**: Suporte para VSCode/Cursor

#### ❌ **Interfaces Não Encontradas**
- **Builder Visual**: Não existe interface gráfica para criação de agentes
- **Wizard por Níveis**: Não há assistente visual para os 5 níveis
- **Templates Visuais**: Não há interface drag-and-drop

### 🚀 Proposta: Agno Agent Builder

Vou criar uma proposta de interface gráfica integrada com IA para auxiliar na criação dos 5 níveis de agentes:

```python
# Proposta de implementação do Agno Agent Builder
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.playground import Playground
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from typing import Dict, List, Any
import streamlit as st
import json

class AgnoAgentBuilder:
    """
    Interface gráfica para criação de agentes Agno por níveis
    Integrada com IA para auxiliar no processo de criação
    """
    
    def __init__(self):
        self.ai_assistant = Agent(
            name="Agno Builder Assistant",
            model=OpenAIChat(id="gpt-4"),
            tools=[DuckDuckGoTools(), CalculatorTools()],
            instructions=[
                "Você é um assistente especializado em criar agentes Agno.",
                "Ajude o usuário a configurar agentes baseado nos 5 níveis.",
                "Sugira ferramentas, instruções e configurações apropriadas.",
                "Explique as melhores práticas para cada nível."
            ]
        )
    
    def render_level_selector(self):
        """Interface para seleção do nível do agente"""
        st.title("🤖 Agno Agent Builder")
        st.markdown("### Selecione o nível do seu agente:")
        
        levels = {
            1: "🛠️ Agentes com ferramentas e instruções",
            2: "📚 Agentes com conhecimento e armazenamento", 
            3: "🧠 Agentes com memória e raciocínio",
            4: "👥 Times de agentes que colaboram",
            5: "🔄 Fluxos de trabalho agênticos com estado"
        }
        
        selected_level = st.selectbox(
            "Nível do Agente:",
            options=list(levels.keys()),
            format_func=lambda x: levels[x]
        )
        
        return selected_level
    
    def render_level_1_builder(self):
        """Builder para Nível 1: Agentes com ferramentas"""
        st.header("🛠️ Nível 1: Agente com Ferramentas")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Configurações Básicas")
            agent_name = st.text_input("Nome do Agente", "Meu Agente")
            agent_role = st.text_input("Função/Papel", "Assistente especializado")
            
            model_provider = st.selectbox(
                "Provedor do Modelo:",
                ["OpenAI", "Anthropic", "Google", "Groq", "Ollama"]
            )
            
            if model_provider == "OpenAI":
                model_id = st.selectbox(
                    "Modelo:",
                    ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"]
                )
            elif model_provider == "Anthropic":
                model_id = st.selectbox(
                    "Modelo:",
                    ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku"]
                )
            
            instructions = st.text_area(
                "Instruções do Agente:",
                "Você é um assistente útil e especializado.",
                height=100
            )
        
        with col2:
            st.subheader("Ferramentas Disponíveis")
            
            tools_categories = {
                "Busca": ["DuckDuckGo", "Google Search", "Exa", "Tavily"],
                "Cálculos": ["Calculator", "Pandas", "NumPy"],
                "Web": ["Firecrawl", "Newspaper4k", "BeautifulSoup"],
                "Financeiro": ["YFinance", "OpenBB", "Alpha Vantage"],
                "Social": ["Email", "Slack", "Discord", "WhatsApp"],
                "Desenvolvimento": ["GitHub", "Docker", "Shell", "Python"]
            }
            
            selected_tools = []
            for category, tools in tools_categories.items():
                st.write(f"**{category}:**")
                for tool in tools:
                    if st.checkbox(f"{tool}", key=f"tool_{tool}"):
                        selected_tools.append(tool)
        
        # Assistente IA
        st.subheader("🤖 Assistente IA")
        if st.button("Obter Sugestões da IA"):
            prompt = f"""
            Estou criando um agente Nível 1 com:
            - Nome: {agent_name}
            - Função: {agent_role}
            - Ferramentas: {selected_tools}
            
            Sugira instruções otimizadas e melhores práticas.
            """
            
            suggestion = self.ai_assistant.run(prompt)
            st.write("**Sugestão da IA:**")
            st.write(suggestion.content)
        
        # Gerar código
        if st.button("Gerar Código do Agente"):
            code = self.generate_level_1_code(
                agent_name, agent_role, model_provider, 
                model_id, instructions, selected_tools
            )
            st.code(code, language="python")
    
    def render_level_2_builder(self):
        """Builder para Nível 2: Agentes com conhecimento"""
        st.header("📚 Nível 2: Agente com Conhecimento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Configurações básicas (reutilizar do nível 1)
            st.subheader("Configurações Básicas")
            agent_name = st.text_input("Nome do Agente", "Agente Especialista")
            
            st.subheader("Base de Conhecimento")
            knowledge_type = st.selectbox(
                "Tipo de Conhecimento:",
                ["Documentos de Texto", "PDFs", "Websites", "CSV/JSON", "YouTube"]
            )
            
            if knowledge_type == "Documentos de Texto":
                knowledge_path = st.text_input("Caminho dos Documentos:", "documentos/")
                chunk_size = st.slider("Tamanho do Chunk:", 100, 2000, 1000)
                chunk_overlap = st.slider("Sobreposição:", 0, 500, 200)
            
            elif knowledge_type == "Websites":
                urls = st.text_area("URLs (uma por linha):", "https://docs.agno.com")
                urls_list = [url.strip() for url in urls.split('\n') if url.strip()]
        
        with col2:
            st.subheader("Banco Vetorial")
            vector_db = st.selectbox(
                "Banco Vetorial:",
                ["ChromaDB", "LanceDB", "PgVector", "Qdrant", "Pinecone"]
            )
            
            embedder = st.selectbox(
                "Modelo de Embeddings:",
                ["OpenAI text-embedding-3-small", "OpenAI text-embedding-ada-002"]
            )
            
            st.subheader("Configurações RAG")
            retrieval_method = st.selectbox(
                "Método de Recuperação:",
                ["Vetorial", "Híbrido", "Palavra-chave"]
            )
            
            top_k = st.slider("Top K Resultados:", 1, 20, 5)
        
        # Assistente IA para RAG
        if st.button("Otimizar Configurações RAG"):
            prompt = f"""
            Estou configurando um sistema RAG com:
            - Tipo de conhecimento: {knowledge_type}
            - Banco vetorial: {vector_db}
            - Método: {retrieval_method}
            
            Sugira as melhores configurações e parâmetros.
            """
            
            suggestion = self.ai_assistant.run(prompt)
            st.write("**Sugestão da IA:**")
            st.write(suggestion.content)
    
    def render_level_3_builder(self):
        """Builder para Nível 3: Agentes com memória"""
        st.header("🧠 Nível 3: Agente com Memória")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Configurações de Memória")
            memory_type = st.multiselect(
                "Tipos de Memória:",
                ["Memória de Sessão", "Memória de Longo Prazo", "Memória Compartilhada"]
            )
            
            storage_type = st.selectbox(
                "Armazenamento:",
                ["SQLite", "PostgreSQL", "MongoDB", "Redis"]
            )
            
            if "Memória de Longo Prazo" in memory_type:
                max_memories = st.slider("Máximo de Memórias:", 100, 10000, 1000)
                summarize_after = st.slider("Resumir após N mensagens:", 5, 50, 10)
        
        with col2:
            st.subheader("Configurações de Raciocínio")
            reasoning_enabled = st.checkbox("Habilitar Raciocínio")
            
            if reasoning_enabled:
                reasoning_type = st.selectbox(
                    "Tipo de Raciocínio:",
                    ["ReasoningTools", "Chain-of-Thought", "Modelo de Raciocínio"]
                )
                
                show_reasoning = st.checkbox("Mostrar Processo de Raciocínio")
    
    def render_level_4_builder(self):
        """Builder para Nível 4: Times de agentes"""
        st.header("👥 Nível 4: Time de Agentes")
        
        st.subheader("Configuração do Time")
        team_name = st.text_input("Nome do Time", "Meu Time de Agentes")
        team_mode = st.selectbox(
            "Modo do Time:",
            ["collaborate", "coordinate", "route"]
        )
        
        st.subheader("Membros do Time")
        num_agents = st.slider("Número de Agentes:", 2, 10, 3)
        
        agents_config = []
        for i in range(num_agents):
            with st.expander(f"Agente {i+1}"):
                name = st.text_input(f"Nome:", f"Agente {i+1}", key=f"agent_name_{i}")
                role = st.text_input(f"Função:", f"Especialista {i+1}", key=f"agent_role_{i}")
                specialization = st.selectbox(
                    f"Especialização:",
                    ["Pesquisa", "Análise", "Escrita", "Cálculos", "Criativo"],
                    key=f"agent_spec_{i}"
                )
                agents_config.append({
                    "name": name,
                    "role": role,
                    "specialization": specialization
                })
        
        # Visualização do fluxo do time
        st.subheader("Fluxo de Trabalho")
        if team_mode == "collaborate":
            st.info("Modo Colaborativo: Todos os agentes trabalham juntos na mesma tarefa")
        elif team_mode == "coordinate":
            st.info("Modo Coordenado: Agentes são coordenados automaticamente")
        elif team_mode == "route":
            st.info("Modo Roteamento: Tarefas são direcionadas para agentes específicos")
    
    def render_level_5_builder(self):
        """Builder para Nível 5: Workflows"""
        st.header("🔄 Nível 5: Workflow Agêntico")
        
        st.subheader("Configuração do Workflow")
        workflow_name = st.text_input("Nome do Workflow", "Meu Workflow")
        workflow_type = st.selectbox(
            "Tipo de Workflow:",
            ["Sequencial", "Paralelo", "Condicional", "Loop", "Híbrido"]
        )
        
        st.subheader("Etapas do Workflow")
        num_steps = st.slider("Número de Etapas:", 2, 10, 3)
        
        steps_config = []
        for i in range(num_steps):
            with st.expander(f"Etapa {i+1}"):
                step_name = st.text_input(f"Nome da Etapa:", f"Etapa {i+1}", key=f"step_name_{i}")
                step_type = st.selectbox(
                    f"Tipo:",
                    ["Agente", "Função", "Condição", "Loop"],
                    key=f"step_type_{i}"
                )
                
                if step_type == "Agente":
                    agent_for_step = st.selectbox(
                        f"Agente:",
                        ["Pesquisador", "Analista", "Editor", "Novo Agente"],
                        key=f"step_agent_{i}"
                    )
                
                dependencies = st.multiselect(
                    f"Depende de:",
                    [f"Etapa {j+1}" for j in range(i)],
                    key=f"step_deps_{i}"
                )
                
                steps_config.append({
                    "name": step_name,
                    "type": step_type,
                    "dependencies": dependencies
                })
        
        # Visualização do workflow
        st.subheader("Visualização do Workflow")
        self.render_workflow_diagram(steps_config)
    
    def render_workflow_diagram(self, steps_config):
        """Renderiza diagrama do workflow"""
        st.write("```mermaid")
        st.write("graph TD")
        for i, step in enumerate(steps_config):
            step_id = f"S{i+1}"
            st.write(f"    {step_id}[{step['name']}]")
            
            for dep in step.get('dependencies', []):
                dep_id = f"S{steps_config.index(next(s for s in steps_config if s['name'] == dep)) + 1}"
                st.write(f"    {dep_id} --> {step_id}")
        st.write("```")
    
    def generate_level_1_code(self, name, role, provider, model, instructions, tools):
        """Gera código Python para agente Nível 1"""
        code = f'''from agno.agent import Agent
from agno.models.{provider.lower()} import {"OpenAIChat" if provider == "OpenAI" else provider}
'''
        
        # Adicionar imports das ferramentas
        tool_imports = {
            "DuckDuckGo": "from agno.tools.duckduckgo import DuckDuckGoTools",
            "Calculator": "from agno.tools.calculator import CalculatorTools",
            "YFinance": "from agno.tools.yfinance import YFinanceTools",
            # Adicionar mais conforme necessário
        }
        
        for tool in tools:
            if tool in tool_imports:
                code += f"{tool_imports[tool]}\n"
        
        code += f'''
# Criar agente {name}
{name.lower().replace(' ', '_')} = Agent(
    name="{name}",
    role="{role}",
    model={"OpenAIChat" if provider == "OpenAI" else provider}(id="{model}"),
    tools=[
'''
        
        # Adicionar ferramentas
        tool_classes = {
            "DuckDuckGo": "DuckDuckGoTools()",
            "Calculator": "CalculatorTools()",
            "YFinance": "YFinanceTools(stock_price=True)",
        }
        
        for tool in tools:
            if tool in tool_classes:
                code += f"        {tool_classes[tool]},\n"
        
        code += f'''    ],
    instructions=[
        "{instructions}"
    ],
    show_tool_calls=True,
    markdown=True,
)

# Testar o agente
{name.lower().replace(' ', '_')}.print_response("Olá! Como você pode me ajudar?")
'''
        
        return code
    
    def run_builder(self):
        """Executa a interface principal do builder"""
        selected_level = self.render_level_selector()
        
        st.markdown("---")
        
        if selected_level == 1:
            self.render_level_1_builder()
        elif selected_level == 2:
            self.render_level_2_builder()
        elif selected_level == 3:
            self.render_level_3_builder()
        elif selected_level == 4:
            self.render_level_4_builder()
        elif selected_level == 5:
            self.render_level_5_builder()
        
        # Botões de ação
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Salvar Configuração"):
                st.success("Configuração salva!")
        
        with col2:
            if st.button("🚀 Testar Agente"):
                st.info("Iniciando teste do agente...")
        
        with col3:
            if st.button("📤 Exportar Código"):
                st.success("Código exportado!")

# Exemplo de uso
if __name__ == "__main__":
    import streamlit as st
    
    builder = AgnoAgentBuilder()
    builder.run_builder()
```

### 🎯 Funcionalidades da Interface Proposta

#### **1. Seletor de Níveis Visual**
- Interface intuitiva para escolher entre os 5 níveis
- Explicação clara de cada nível
- Progressão lógica de complexidade

#### **2. Builders Especializados por Nível**
- **Nível 1**: Configurador de ferramentas com checkboxes
- **Nível 2**: Builder de RAG com configurações visuais
- **Nível 3**: Configurador de memória e raciocínio
- **Nível 4**: Designer de times com fluxograma
- **Nível 5**: Editor de workflows com diagrama

#### **3. Assistente IA Integrado**
- IA especializada em Agno para sugestões
- Otimização automática de configurações
- Explicação de melhores práticas
- Geração de código personalizado

#### **4. Recursos Visuais**
- Diagramas de fluxo para workflows
- Visualização de arquitetura de times
- Preview de configurações
- Templates pré-configurados

#### **5. Exportação e Teste**
- Geração automática de código Python
- Teste integrado no playground
- Salvamento de configurações
- Compartilhamento de templates

### 📋 Implementação Sugerida

Para implementar esta interface, seria necessário:

1. **Criar módulo `agno.builder`**
2. **Integrar com Streamlit ou FastAPI**
3. **Desenvolver componentes visuais**
4. **Integrar com o playground existente**
5. **Adicionar templates e exemplos**

Esta proposta aproveitaria a arquitetura existente do Agno e forneceria uma interface visual completa para criação de agentes por níveis, com assistência de IA integrada.

---

## Recursos e Comunidade

### 📚 Documentação Oficial

- **Site Principal**: https://docs.agno.com
- **Exemplos**: https://docs.agno.com/examples
- **API Reference**: https://docs.agno.com/api
- **Guias**: https://docs.agno.com/guides

### 💬 Comunidade

- **Discord**: https://discord.gg/4MtYHHrgA8
- **Fórum**: https://community.agno.com
- **GitHub**: https://github.com/agno-agi/agno
- **Twitter**: @agno_agi

### 🎓 Aprendizado

```python
# Recursos de aprendizado integrados
from agno.learning import AgnoTutorial

# Tutorial interativo
tutorial = AgnoTutorial()
tutorial.start_basic_agent_tutorial()

# Exemplos contextuais
from agno.examples import load_example

# Carregar exemplo específico
exemplo_rag = load_example("rag_agent")
exemplo_team = load_example("agent_team")
exemplo_workflow = load_example("workflow_basic")
```

### 🔧 Ferramentas de Desenvolvimento

```python
# CLI do Agno
# pip install agno[cli]

# Comandos úteis:
# agno init meu_projeto          # Criar novo projeto
# agno run agent.py             # Executar agente
# agno test                     # Executar testes
# agno deploy                   # Deploy para produção
# agno monitor                  # Monitorar agentes
```

### 📊 Templates e Starters

```python
# Templates prontos para uso
from agno.templates import (
    ChatbotTemplate,
    RAGTemplate,
    WorkflowTemplate,
    TeamTemplate
)

# Chatbot básico
chatbot = ChatbotTemplate(
    model="gpt-4",
    personality="amigável e útil",
    domain="atendimento ao cliente"
)

# Sistema RAG
rag_system = RAGTemplate(
    knowledge_path="documentos/",
    model="gpt-4",
    retrieval_method="hybrid"
)

# Workflow de análise
analysis_workflow = WorkflowTemplate(
    type="data_analysis",
    steps=["collect", "analyze", "report"],
    agents=["researcher", "analyst", "reporter"]
)
```

---

## Conclusão

O Agno Framework oferece uma plataforma completa e poderosa para construção de sistemas agênticos avançados. Com suas interfaces visuais intuitivas, ampla gama de ferramentas e arquitetura flexível, você pode criar desde agentes simples até sistemas complexos de múltiplos agentes.

### 🚀 Próximos Passos

1. **Instale o Agno** e configure suas chaves de API
2. **Experimente os exemplos** deste manual
3. **Explore o cookbook** oficial para mais casos de uso
4. **Junte-se à comunidade** para aprender e compartilhar
5. **Monitore seus agentes** na plataforma oficial
6. **Contribua** com o projeto open-source

### 💡 Dicas Finais

- Comece simples e evolua gradualmente
- Use monitoramento desde o início
- Documente seus agentes e workflows
- Teste regularmente em diferentes cenários
- Mantenha-se atualizado com as novidades

**Boa sorte construindo seus sistemas agênticos com o Agno! 🤖✨**

---

*Este manual foi criado com base na documentação oficial do Agno Framework. Para informações mais atualizadas, consulte sempre https://docs.agno.com*