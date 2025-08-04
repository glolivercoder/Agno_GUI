# 📚 Instruções Completas - Agno Framework

## 🎯 O que é o Agno Framework?

O **Agno** é um framework Python full-stack para construção de Sistemas Multi-Agentes com memória, conhecimento e raciocínio. Ele permite criar desde agentes simples até sistemas complexos de múltiplos agentes que colaboram entre si.

### 🏗️ Os 5 Níveis de Sistemas Agênticos

1. **Nível 1**: 🛠️ Agentes com ferramentas e instruções
2. **Nível 2**: 📚 Agentes com conhecimento e RAG
3. **Nível 3**: 🧠 Agentes com memória e raciocínio
4. **Nível 4**: 👥 Times de agentes colaborativos
5. **Nível 5**: 🔄 Workflows agênticos com estado

---

## 🚀 Primeiros Passos

### 1. Instalação
```bash
pip install agno
```

### 2. Configurar APIs
```bash
# OpenAI
export OPENAI_API_KEY="sk-proj-sua_chave"

# Anthropic
export ANTHROPIC_API_KEY="sk-ant-api03-sua_chave"

# Google Gemini
export GOOGLE_API_KEY="AIzaSy-sua_chave"

# OpenRouter (acesso a 100+ modelos)
export OPENAI_API_KEY="sk-or-v1-sua_chave"
```

### 3. Primeiro Agente
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat

agent = Agent(
    model=OpenAIChat(id="gpt-4"),
    instructions=["Você é um assistente útil."]
)

response = agent.run("Olá! Como você funciona?")
print(response.content)
```

---

## 📋 Exemplos por Nível

### 🛠️ Nível 1: Agentes com Ferramentas

#### Exemplo 1: Assistente de Pesquisa
```python
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools

pesquisador = Agent(
    name="Assistente de Pesquisa",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools(), CalculatorTools()],
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
response = pesquisador.run(
    "Pesquise sobre o PIB do Brasil em 2024 e calcule a diferença percentual com 2023"
)
print(response.content)
```

#### Exemplo 2: Analista Financeiro
```python
from agno.tools.yfinance import YFinanceTools

analista_financeiro = Agent(
    name="Analista Financeiro",
    model=OpenAIChat(id="gpt-4"),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            company_info=True,
            company_news=True
        ),
        CalculatorTools()
    ],
    instructions=[
        "Você é um analista financeiro especializado.",
        "Use dados reais do mercado para suas análises.",
        "Sempre inclua métricas importantes como P/E, ROE, etc.",
        "Forneça recomendações baseadas em dados."
    ],
    markdown=True,
)

# Exemplo de uso
response = analista_financeiro.run(
    "Analise as ações da Apple (AAPL) e forneça uma recomendação de investimento"
)
```

---

### 📚 Nível 2: Agentes com Conhecimento (RAG)

#### Exemplo 1: Especialista em Documentação
```python
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.chroma import ChromaDb

# Criar base de conhecimento
knowledge_base = TextKnowledgeBase(
    path="documentos/",
    vector_db=ChromaDb(
        collection="empresa_docs",
        path="vectordb/"
    )
)

especialista_docs = Agent(
    name="Especialista em Documentação",
    model=OpenAIChat(id="gpt-4"),
    knowledge=knowledge_base,
    instructions=[
        "Você é um especialista na documentação da empresa.",
        "Use apenas informações da base de conhecimento.",
        "Sempre referencie a fonte das informações.",
        "Se não souber, diga que não está na base de conhecimento."
    ],
    markdown=True,
)

# Exemplo de uso
response = especialista_docs.run(
    "Quais são as políticas de trabalho remoto da nossa empresa?"
)
```

#### Exemplo 2: Assistente de Código
```python
from agno.knowledge.pdf import PDFKnowledgeBase

# Base de conhecimento com PDFs técnicos
code_knowledge = PDFKnowledgeBase(
    path="documentacao_tecnica/",
    chunk_size=1000,
    chunk_overlap=200
)

assistente_codigo = Agent(
    name="Assistente de Código",
    model=OpenAIChat(id="gpt-4"),
    knowledge=code_knowledge,
    tools=[DuckDuckGoTools()],
    instructions=[
        "Você é um assistente de programação especializado.",
        "Use a documentação técnica como referência principal.",
        "Forneça exemplos de código práticos e funcionais.",
        "Explique conceitos complexos de forma simples."
    ],
    markdown=True,
)

# Exemplo de uso
response = assistente_codigo.run(
    "Como implementar autenticação JWT em Python usando FastAPI?"
)
```

---

### 🧠 Nível 3: Agentes com Memória e Raciocínio

#### Exemplo 1: Assistente Pessoal com Memória
```python
from agno.memory import Memory
from agno.storage.sqlite import SqliteStorage
from agno.tools.reasoning import ReasoningTools

# Configurar armazenamento
storage = SqliteStorage(
    table_name="conversas_assistente",
    db_file="memoria_assistente.db"
)

assistente_pessoal = Agent(
    name="Assistente Pessoal",
    model=OpenAIChat(id="gpt-4"),
    storage=storage,
    tools=[ReasoningTools(add_instructions=True), DuckDuckGoTools()],
    add_history_to_messages=True,
    instructions=[
        "Você é um assistente pessoal com memória.",
        "Lembre-se das conversas anteriores.",
        "Use o contexto histórico para personalizar respostas.",
        "Pense antes de agir usando o raciocínio estruturado.",
        "Mantenha um tom consistente ao longo das sessões."
    ],
    show_tool_calls=True,
    markdown=True,
)

# Primeira conversa
response1 = assistente_pessoal.run("Meu nome é João e trabalho com marketing digital.")

# Segunda conversa (em outra sessão)
response2 = assistente_pessoal.run("Você lembra qual é minha área de trabalho?")
```

#### Exemplo 2: Agente de Raciocínio Avançado
```python
agente_raciocinante = Agent(
    name="Analista Estratégico",
    model=OpenAIChat(id="gpt-4"),
    tools=[
        ReasoningTools(add_instructions=True),
        DuckDuckGoTools(),
        YFinanceTools(),
        CalculatorTools()
    ],
    instructions=[
        "Você é um analista estratégico que pensa antes de agir.",
        "Use o raciocínio estruturado para resolver problemas complexos.",
        "Mostre seu processo de pensamento passo a passo.",
        "Valide suas conclusões com dados reais.",
        "Considere múltiplas perspectivas antes de decidir."
    ],
    show_tool_calls=True,
    markdown=True,
)

# Exemplo complexo
response = agente_raciocinante.run(
    "Analise se vale a pena investir em ações da Tesla considerando "
    "os dados financeiros atuais, tendências do mercado de carros elétricos "
    "e fatores macroeconômicos. Forneça uma recomendação fundamentada.",
    show_full_reasoning=True
)
```

---

### 👥 Nível 4: Times de Agentes

#### Exemplo 1: Time de Pesquisa Colaborativo
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
        "Foque em dados factuais e estatísticas."
    ]
)

# Agente Analista
analista = Agent(
    name="Analista",
    role="Analisa dados e faz cálculos",
    model=OpenAIChat(id="gpt-4"),
    tools=[CalculatorTools()],
    instructions=[
        "Analise dados de forma estruturada.",
        "Faça cálculos precisos e relevantes.",
        "Identifique tendências e padrões."
    ]
)

# Agente Editor
editor = Agent(
    name="Editor",
    role="Compila e formata relatórios",
    model=OpenAIChat(id="gpt-4"),
    instructions=[
        "Compile informações de outros agentes.",
        "Crie relatórios bem estruturados e legíveis.",
        "Use formatação markdown adequada.",
        "Garanta coerência e fluidez no texto."
    ]
)

# Criar time colaborativo
time_pesquisa = Team(
    members=[pesquisador, analista, editor],
    model=OpenAIChat(id="gpt-4"),
    mode="collaborate",
    instructions=[
        "Trabalhem juntos para criar relatórios completos.",
        "Cada agente deve contribuir com sua especialidade.",
        "O editor deve compilar o trabalho final.",
        "Garantam qualidade e precisão nas informações."
    ],
    show_tool_calls=True,
    markdown=True
)

# Usar o time
response = time_pesquisa.run(
    "Criem um relatório sobre o mercado de carros elétricos no Brasil, "
    "incluindo dados de vendas, principais players e projeções futuras."
)
```

#### Exemplo 2: Time Especializado em Finanças
```python
# Analista Técnico
analista_tecnico = Agent(
    name="Analista Técnico",
    role="Análise técnica de ações",
    model=OpenAIChat(id="gpt-4"),
    tools=[YFinanceTools(stock_price=True, company_info=True)],
    instructions=[
        "Foque em análise técnica: gráficos, tendências, suporte/resistência.",
        "Use indicadores técnicos como RSI, MACD, médias móveis.",
        "Identifique padrões de preço e volume."
    ]
)

# Analista Fundamentalista
analista_fundamentalista = Agent(
    name="Analista Fundamentalista",
    role="Análise fundamentalista",
    model=OpenAIChat(id="gpt-4"),
    tools=[YFinanceTools(financials=True, balance_sheet=True), CalculatorTools()],
    instructions=[
        "Analise fundamentos: receita, lucro, dívida, crescimento.",
        "Calcule métricas como P/E, P/B, ROE, ROA.",
        "Avalie a saúde financeira da empresa."
    ]
)

# Estrategista
estrategista = Agent(
    name="Estrategista",
    role="Estratégia de investimento",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Combine análises técnica e fundamentalista.",
        "Considere fatores macroeconômicos.",
        "Forneça recomendações de investimento claras."
    ]
)

time_financeiro = Team(
    members=[analista_tecnico, analista_fundamentalista, estrategista],
    model=OpenAIChat(id="gpt-4"),
    mode="coordinate",
    success_criteria="Relatório completo com análise técnica, fundamentalista e recomendação final",
    instructions=[
        "Coordenem análises complementares.",
        "Evitem duplicação de esforços.",
        "Integrem diferentes perspectivas de análise."
    ],
    show_tool_calls=True,
    markdown=True
)

# Exemplo de uso
response = time_financeiro.run(
    "Analisem as ações da Microsoft (MSFT) e forneçam uma recomendação "
    "de investimento completa considerando análise técnica e fundamentalista."
)
```

---

### 🔄 Nível 5: Workflows Agênticos

#### Exemplo 1: Workflow de Análise de Mercado
```python
from agno.workflow import Workflow
from agno.workflow.task import Task

# Definir agentes especializados
pesquisador_mercado = Agent(
    name="Pesquisador de Mercado",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=["Pesquise tendências e dados de mercado atuais."]
)

analista_competitivo = Agent(
    name="Analista Competitivo",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools(), CalculatorTools()],
    instructions=["Analise concorrentes e posicionamento de mercado."]
)

estrategista_negocio = Agent(
    name="Estrategista de Negócio",
    model=OpenAIChat(id="gpt-4"),
    instructions=["Desenvolva estratégias baseadas nas análises anteriores."]
)

# Definir tarefas do workflow
tarefa_pesquisa = Task(
    name="pesquisa_mercado",
    agent=pesquisador_mercado,
    description="Pesquisar dados e tendências do mercado alvo"
)

tarefa_analise_competitiva = Task(
    name="analise_competitiva",
    agent=analista_competitivo,
    description="Analisar concorrentes e posicionamento",
    depends_on=["pesquisa_mercado"]
)

tarefa_estrategia = Task(
    name="desenvolvimento_estrategia",
    agent=estrategista_negocio,
    description="Desenvolver estratégia de negócio",
    depends_on=["pesquisa_mercado", "analise_competitiva"]
)

# Criar workflow
workflow_analise = Workflow(
    name="Análise Estratégica de Mercado",
    tasks=[tarefa_pesquisa, tarefa_analise_competitiva, tarefa_estrategia]
)

# Executar workflow
resultado = workflow_analise.run(
    input_data={"mercado": "Inteligência Artificial no Brasil"}
)
```

#### Exemplo 2: Workflow de Desenvolvimento de Produto
```python
from agno.workflow.condition import Condition

# Agentes especializados
pesquisador_usuario = Agent(
    name="Pesquisador de Usuário",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=["Pesquise necessidades e comportamentos dos usuários."]
)

designer_produto = Agent(
    name="Designer de Produto",
    model=OpenAIChat(id="gpt-4"),
    instructions=["Projete soluções baseadas na pesquisa de usuários."]
)

analista_viabilidade = Agent(
    name="Analista de Viabilidade",
    model=OpenAIChat(id="gpt-4"),
    tools=[CalculatorTools()],
    instructions=["Analise viabilidade técnica e financeira."]
)

# Tarefas com condições
tarefa_pesquisa_usuario = Task(
    name="pesquisa_usuario",
    agent=pesquisador_usuario,
    description="Pesquisar necessidades dos usuários"
)

tarefa_design_inicial = Task(
    name="design_inicial",
    agent=designer_produto,
    description="Criar design inicial do produto",
    depends_on=["pesquisa_usuario"]
)

tarefa_analise_viabilidade = Task(
    name="analise_viabilidade",
    agent=analista_viabilidade,
    description="Analisar viabilidade do design",
    depends_on=["design_inicial"]
)

# Condição para redesign
def precisa_redesign(context):
    return context.get("viabilidade_score", 0) < 0.7

tarefa_redesign = Task(
    name="redesign",
    agent=designer_produto,
    description="Redesenhar produto baseado na análise",
    depends_on=["analise_viabilidade"],
    condition=Condition(check=precisa_redesign)
)

# Workflow condicional
workflow_produto = Workflow(
    name="Desenvolvimento de Produto",
    tasks=[
        tarefa_pesquisa_usuario,
        tarefa_design_inicial,
        tarefa_analise_viabilidade,
        tarefa_redesign
    ]
)

# Executar
resultado = workflow_produto.run(
    input_data={"produto": "App de produtividade para desenvolvedores"}
)
```

---

## 🌟 Exemplos da Comunidade

### 1. Agente de Atendimento ao Cliente
```python
# Baseado em exemplo da comunidade Agno
from agno.knowledge.website import WebsiteKnowledgeBase

atendimento = Agent(
    name="Assistente de Atendimento",
    model=OpenAIChat(id="gpt-4"),
    knowledge=WebsiteKnowledgeBase(
        urls=["https://empresa.com/faq", "https://empresa.com/politicas"]
    ),
    instructions=[
        "Você é um assistente de atendimento ao cliente.",
        "Seja sempre educado e prestativo.",
        "Use informações da base de conhecimento da empresa.",
        "Se não souber algo, direcione para um humano."
    ]
)
```

### 2. Agente de Análise de Sentimentos
```python
# Exemplo popular da comunidade
from agno.tools.twitter import TwitterTools

analista_sentimentos = Agent(
    name="Analista de Sentimentos",
    model=OpenAIChat(id="gpt-4"),
    tools=[TwitterTools(), DuckDuckGoTools()],
    instructions=[
        "Analise sentimentos em redes sociais.",
        "Classifique como positivo, negativo ou neutro.",
        "Identifique tendências e padrões.",
        "Forneça insights acionáveis."
    ]
)
```

### 3. Agente de Tradução Inteligente
```python
# Exemplo avançado da comunidade
tradutor_inteligente = Agent(
    name="Tradutor Contextual",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=[
        "Traduza considerando contexto cultural.",
        "Pesquise termos técnicos quando necessário.",
        "Mantenha o tom e estilo do texto original.",
        "Explique escolhas de tradução quando relevante."
    ]
)
```

---

## 🎯 Prompts de Exemplo para Cada Nível

### Nível 1 - Prompts para Agentes com Ferramentas
```
"Crie um agente que pesquise informações sobre [TÓPICO] na web e calcule estatísticas relevantes."

"Desenvolva um assistente financeiro que analise ações da [EMPRESA] e forneça recomendações."

"Construa um agente que monitore preços de criptomoedas e alerte sobre mudanças significativas."
```

### Nível 2 - Prompts para Agentes com Conhecimento
```
"Crie um especialista em [ÁREA] que use documentos da empresa para responder perguntas."

"Desenvolva um assistente de código que consulte documentação técnica para ajudar programadores."

"Construa um agente que analise contratos legais usando uma base de conhecimento jurídica."
```

### Nível 3 - Prompts para Agentes com Memória
```
"Crie um assistente pessoal que lembre das preferências do usuário ao longo do tempo."

"Desenvolva um agente de vendas que mantenha histórico de interações com clientes."

"Construa um tutor que adapte o ensino baseado no progresso do aluno."
```

### Nível 4 - Prompts para Times de Agentes
```
"Crie um time de análise de mercado com pesquisador, analista e estrategista."

"Desenvolva uma equipe de desenvolvimento com arquiteto, desenvolvedor e testador."

"Construa um time de marketing com criativo, analista e gerente de campanha."
```

### Nível 5 - Prompts para Workflows
```
"Crie um workflow de análise de investimentos com validação e aprovação em etapas."

"Desenvolva um processo de desenvolvimento de produto com pesquisa, design e validação."

"Construa um workflow de atendimento ao cliente com triagem, resolução e follow-up."
```

---

## 🔧 Dicas Avançadas

### Performance
- Use modelos menores para tarefas simples
- Implemente cache para respostas frequentes
- Otimize prompts para reduzir tokens

### Segurança
- Valide inputs do usuário
- Use sandboxing para execução de código
- Implemente rate limiting

### Monitoramento
- Use logs estruturados
- Monitore custos de API
- Implemente métricas de performance

### Escalabilidade
- Use processamento assíncrono
- Implemente load balancing
- Configure auto-scaling

---

## 📚 Recursos Adicionais

- **Documentação Oficial**: https://docs.agno.com
- **Exemplos no GitHub**: https://github.com/agno-agi/agno/tree/main/cookbook
- **Comunidade Discord**: https://discord.gg/4MtYHHrgA8
- **Fórum da Comunidade**: https://community.agno.com

---

## 🎉 Conclusão

O Agno Framework oferece uma progressão natural desde agentes simples até sistemas complexos. Comece com o Nível 1 e evolua gradualmente conforme suas necessidades crescem. A comunidade ativa e os exemplos práticos facilitam o aprendizado e implementação.

**Próximos passos:**
1. Experimente os exemplos básicos
2. Adapte para seu caso de uso
3. Explore funcionalidades avançadas
4. Contribua com a comunidade

Boa sorte construindo seus agentes inteligentes! 🚀