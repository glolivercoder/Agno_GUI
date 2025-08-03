#!/usr/bin/env python3
"""
Exemplo básico do Agno Framework
Demonstra como criar diferentes tipos de agentes
"""

import os
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.knowledge.text import TextKnowledgeBase
from agno.memory import Memory
from agno.storage.sqlite import SqliteStorage

def exemplo_agente_basico():
    """Exemplo de um agente básico"""
    print("🤖 Criando Agente Básico...")
    
    agent = Agent(
        model=OpenAIChat(id="gpt-3.5-turbo"),
        instructions=[
            "Você é um assistente útil e amigável.",
            "Responda de forma concisa e clara.",
            "Use emojis quando apropriado."
        ],
        markdown=True,
    )
    
    print(f"✅ Agente criado: {agent.model.id}")
    return agent

def exemplo_agente_com_ferramentas():
    """Exemplo de agente com ferramentas"""
    print("🔧 Criando Agente com Ferramentas...")
    
    agent = Agent(
        model=OpenAIChat(id="gpt-3.5-turbo"),
        tools=[
            DuckDuckGoTools(),
            CalculatorTools()
        ],
        instructions=[
            "Você é um assistente de pesquisa e cálculos.",
            "Use as ferramentas disponíveis quando necessário.",
            "Sempre cite suas fontes quando fizer pesquisas."
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    print(f"✅ Agente com ferramentas criado: {len(agent.tools)} ferramentas")
    return agent

def exemplo_agente_com_conhecimento():
    """Exemplo de agente com base de conhecimento"""
    print("📚 Criando Agente com Conhecimento...")
    
    # Criar uma base de conhecimento simples
    knowledge_base = TextKnowledgeBase(
        path="conhecimento_exemplo.txt",
        vector_db=None  # Usará ChromaDB por padrão
    )
    
    agent = Agent(
        model=OpenAIChat(id="gpt-3.5-turbo"),
        knowledge=knowledge_base,
        instructions=[
            "Você é um especialista que usa a base de conhecimento fornecida.",
            "Sempre referencie a fonte quando usar informações da base de conhecimento.",
            "Se não souber algo, diga que não está na sua base de conhecimento."
        ],
        markdown=True,
    )
    
    print(f"✅ Agente com conhecimento criado")
    return agent

def exemplo_agente_com_memoria():
    """Exemplo de agente com memória"""
    print("🧠 Criando Agente com Memória...")
    
    # Criar storage primeiro
    storage = SqliteStorage(table_name="agent_sessions", db_file="agno_memory.db")
    
    agent = Agent(
        model=OpenAIChat(id="gpt-3.5-turbo"),
        storage=storage,
        add_history_to_messages=True,
        instructions=[
            "Você é um assistente com memória.",
            "Lembre-se das conversas anteriores com o usuário.",
            "Use o contexto das conversas passadas para dar respostas mais personalizadas."
        ],
        markdown=True,
    )
    
    print(f"✅ Agente com memória criado")
    return agent

def exemplo_time_de_agentes():
    """Exemplo de time de agentes"""
    print("👥 Criando Time de Agentes...")
    
    # Agente pesquisador
    pesquisador = Agent(
        name="Pesquisador",
        role="Pesquisa informações na web",
        model=OpenAIChat(id="gpt-3.5-turbo"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é um pesquisador especializado.",
            "Sempre inclua fontes nas suas pesquisas.",
            "Seja preciso e objetivo."
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Agente analista
    analista = Agent(
        name="Analista",
        role="Analisa dados e faz cálculos",
        model=OpenAIChat(id="gpt-3.5-turbo"),
        tools=[CalculatorTools()],
        instructions=[
            "Você é um analista de dados.",
            "Faça cálculos precisos e análises detalhadas.",
            "Use tabelas para apresentar dados quando apropriado."
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    # Criar o time
    team = Team(
        members=[pesquisador, analista],
        model=OpenAIChat(id="gpt-3.5-turbo"),
        instructions=[
            "Trabalhem juntos para fornecer respostas completas.",
            "O pesquisador deve buscar informações e o analista deve analisá-las.",
            "Sempre incluam fontes e cálculos quando relevante."
        ],
        show_tool_calls=True,
        markdown=True,
    )
    
    print(f"✅ Time criado com {len(team.members)} agentes")
    return team

def criar_arquivo_conhecimento():
    """Cria um arquivo de exemplo para a base de conhecimento"""
    conteudo = """
# Base de Conhecimento - Agno Framework

## O que é o Agno?
O Agno é um framework Python para construção de sistemas multi-agentes com memória, conhecimento e raciocínio.

## Características Principais:
- Suporte a 23+ provedores de modelos
- Instantiação rápida (~3μs)
- Baixo uso de memória (~6.5Kib)
- Suporte multimodal nativo
- RAG agêntico integrado
- Sistema de memória persistente

## Níveis de Sistemas Agênticos:
1. Agentes com ferramentas e instruções
2. Agentes com conhecimento e armazenamento
3. Agentes com memória e raciocínio
4. Times de agentes que colaboram
5. Fluxos de trabalho agênticos com estado

## Casos de Uso:
- Assistentes de pesquisa
- Análise de documentos
- Automação de tarefas
- Chatbots inteligentes
- Sistemas de suporte
"""
    
    with open("conhecimento_exemplo.txt", "w", encoding="utf-8") as f:
        f.write(conteudo)
    
    print("📄 Arquivo de conhecimento criado: conhecimento_exemplo.txt")

def main():
    """Função principal"""
    print("🚀 Exemplos do Agno Framework")
    print("=" * 50)
    
    # Verificar se as chaves de API estão configuradas
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️  OPENAI_API_KEY não configurada. Os exemplos não farão chamadas reais.")
        print("   Para testar completamente, configure: export OPENAI_API_KEY=sua_chave")
    
    print()
    
    # Criar arquivo de conhecimento
    criar_arquivo_conhecimento()
    print()
    
    # Exemplos de diferentes tipos de agentes
    try:
        agente_basico = exemplo_agente_basico()
        print()
        
        agente_ferramentas = exemplo_agente_com_ferramentas()
        print()
        
        agente_conhecimento = exemplo_agente_com_conhecimento()
        print()
        
        agente_memoria = exemplo_agente_com_memoria()
        print()
        
        time_agentes = exemplo_time_de_agentes()
        print()
        
        print("🎉 Todos os exemplos foram criados com sucesso!")
        print("\n📝 Próximos passos:")
        print("1. Configure sua OPENAI_API_KEY para testar os agentes")
        print("2. Use agent.print_response('sua pergunta') para interagir")
        print("3. Use team.print_response('sua pergunta') para usar o time")
        print("4. Explore mais exemplos em: https://docs.agno.com/examples")
        
    except Exception as e:
        print(f"❌ Erro ao criar exemplos: {e}")

if __name__ == "__main__":
    main()