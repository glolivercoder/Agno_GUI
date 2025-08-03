#!/usr/bin/env python3
"""
Teste básico do Agno Framework
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

def test_basic_agent():
    """Teste básico de um agente Agno"""
    try:
        # Criar um agente básico
        agent = Agent(
            model=OpenAIChat(id="gpt-3.5-turbo"),
            instructions=[
                "Você é um assistente útil e amigável.",
                "Responda de forma concisa e clara."
            ],
            markdown=True,
        )
        
        print("✅ Agente criado com sucesso!")
        print(f"Modelo: {agent.model.id}")
        print(f"Instruções: {len(agent.instructions)} instruções configuradas")
        
        # Teste sem fazer chamada real (para não precisar de API key)
        print("✅ Agno instalado e configurado corretamente!")
        
    except Exception as e:
        print(f"❌ Erro ao criar agente: {e}")
        return False
    
    return True

def test_imports():
    """Testa se as importações principais funcionam"""
    try:
        from agno.agent import Agent
        from agno.team import Team
        from agno.models.openai import OpenAIChat
        from agno.models.anthropic import Claude
        from agno.tools.duckduckgo import DuckDuckGoTools
        from agno.knowledge.pdf import PDFKnowledgeBase
        from agno.memory import Memory
        from agno.storage.sqlite import SqliteStorage
        
        print("✅ Todas as importações principais funcionaram!")
        return True
        
    except ImportError as e:
        print(f"❌ Erro na importação: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Testando instalação do Agno Framework...")
    print("=" * 50)
    
    # Teste de importações
    print("\n1. Testando importações...")
    imports_ok = test_imports()
    
    # Teste de criação de agente
    print("\n2. Testando criação de agente...")
    agent_ok = test_basic_agent()
    
    print("\n" + "=" * 50)
    if imports_ok and agent_ok:
        print("🎉 Agno Framework instalado e funcionando corretamente!")
        print("\n📚 Próximos passos:")
        print("1. Configure suas chaves de API (OPENAI_API_KEY, ANTHROPIC_API_KEY, etc.)")
        print("2. Explore os exemplos em: https://docs.agno.com/examples")
        print("3. Consulte a documentação completa em: https://docs.agno.com")
    else:
        print("❌ Problemas encontrados na instalação.")