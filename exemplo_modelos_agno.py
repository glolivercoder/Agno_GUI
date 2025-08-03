#!/usr/bin/env python3
"""
Exemplo de uso dos diferentes provedores de modelos no Agno Framework
Demonstra como usar OpenAI, Anthropic, Google Gemini e OpenRouter
"""

import os
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openrouter import OpenRouter
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools

def exemplo_openai():
    """Exemplo usando OpenAI GPT"""
    print("🔵 Testando OpenAI GPT-4...")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ OPENAI_API_KEY não configurada")
        return
    
    agent = Agent(
        name="Assistente OpenAI",
        model=OpenAIChat(id="gpt-4"),
        tools=[DuckDuckGoTools(), CalculatorTools()],
        instructions=[
            "Você é um assistente OpenAI.",
            "Use as ferramentas quando necessário.",
            "Seja conciso e útil."
        ],
        markdown=True,
    )
    
    try:
        response = agent.run("Olá! Qual é a capital do Brasil?")
        print(f"✅ Resposta OpenAI: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Erro OpenAI: {e}")

def exemplo_anthropic():
    """Exemplo usando Anthropic Claude"""
    print("\n🟠 Testando Anthropic Claude...")
    
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️ ANTHROPIC_API_KEY não configurada")
        return
    
    agent = Agent(
        name="Assistente Claude",
        model=Claude(id="claude-3-5-sonnet"),
        tools=[CalculatorTools()],
        instructions=[
            "Você é Claude, um assistente da Anthropic.",
            "Seja analítico e preciso.",
            "Use cálculos quando apropriado."
        ],
        markdown=True,
    )
    
    try:
        response = agent.run("Calcule 15% de 250 e explique o resultado.")
        print(f"✅ Resposta Claude: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Erro Claude: {e}")

def exemplo_google_gemini():
    """Exemplo usando Google Gemini"""
    print("\n🔴 Testando Google Gemini...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ GOOGLE_API_KEY não configurada")
        return
    
    agent = Agent(
        name="Assistente Gemini",
        model=Gemini(id="gemini-2.0-flash-001"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "Você é Gemini, assistente do Google.",
            "Seja informativo e preciso.",
            "Use pesquisas para informações atuais."
        ],
        markdown=True,
    )
    
    try:
        response = agent.run("Pesquise sobre as últimas novidades em IA.")
        print(f"✅ Resposta Gemini: {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Erro Gemini: {e}")

def exemplo_openrouter():
    """Exemplo usando OpenRouter"""
    print("\n🌐 Testando OpenRouter...")
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("⚠️ OPENROUTER_API_KEY não configurada")
        return
    
    # Exemplo com modelo gratuito
    agent_free = Agent(
        name="Assistente OpenRouter Gratuito",
        model=OpenRouter(id="meta-llama/llama-3.1-8b-instruct:free"),
        instructions=[
            "Você é um assistente usando modelo gratuito via OpenRouter.",
            "Seja útil e eficiente."
        ],
        markdown=True,
    )
    
    try:
        response = agent_free.run("Explique o que é inteligência artificial em 2 frases.")
        print(f"✅ Resposta OpenRouter (Gratuito): {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Erro OpenRouter (Gratuito): {e}")
    
    # Exemplo com modelo pago (GPT-4 via OpenRouter)
    agent_paid = Agent(
        name="Assistente OpenRouter Premium",
        model=OpenRouter(id="openai/gpt-4o"),
        tools=[DuckDuckGoTools(), CalculatorTools()],
        instructions=[
            "Você é um assistente premium via OpenRouter.",
            "Use todas as ferramentas disponíveis.",
            "Forneça respostas detalhadas."
        ],
        markdown=True,
    )
    
    try:
        response = agent_paid.run("Faça uma pesquisa sobre Python e calcule quantos anos tem a linguagem.")
        print(f"✅ Resposta OpenRouter (Premium): {response.content[:100]}...")
    except Exception as e:
        print(f"❌ Erro OpenRouter (Premium): {e}")

def exemplo_comparacao_modelos():
    """Compara respostas de diferentes modelos"""
    print("\n🔄 Comparando Modelos...")
    
    pergunta = "Explique machine learning em uma frase simples."
    
    modelos = []
    
    # Adicionar modelos disponíveis
    if os.getenv("OPENAI_API_KEY"):
        modelos.append(("OpenAI GPT-4", OpenAIChat(id="gpt-4")))
    
    if os.getenv("ANTHROPIC_API_KEY"):
        modelos.append(("Claude 3.5", Claude(id="claude-3-5-sonnet")))
    
    if os.getenv("GOOGLE_API_KEY"):
        modelos.append(("Gemini 2.0", Gemini(id="gemini-2.0-flash-001")))
    
    if os.getenv("OPENROUTER_API_KEY"):
        modelos.append(("OpenRouter Llama", OpenRouter(id="meta-llama/llama-3.1-8b-instruct:free")))
    
    for nome, modelo in modelos:
        try:
            agent = Agent(
                model=modelo,
                instructions=["Seja conciso e claro."],
                markdown=True
            )
            
            response = agent.run(pergunta)
            print(f"\n**{nome}:**")
            print(f"{response.content}")
            
        except Exception as e:
            print(f"\n**{nome}:** ❌ Erro: {e}")

def verificar_configuracao():
    """Verifica quais chaves de API estão configuradas"""
    print("🔍 Verificando Configuração de APIs...")
    
    apis = {
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY", 
        "Google": "GOOGLE_API_KEY",
        "OpenRouter": "OPENROUTER_API_KEY"
    }
    
    configuradas = []
    nao_configuradas = []
    
    for nome, var in apis.items():
        if os.getenv(var):
            configuradas.append(f"✅ {nome}")
        else:
            nao_configuradas.append(f"❌ {nome}")
    
    print("\n**APIs Configuradas:**")
    for api in configuradas:
        print(f"  {api}")
    
    print("\n**APIs Não Configuradas:**")
    for api in nao_configuradas:
        print(f"  {api}")
    
    if nao_configuradas:
        print("\n💡 **Para configurar:**")
        print("export OPENAI_API_KEY=sua_chave_openai")
        print("export ANTHROPIC_API_KEY=sua_chave_anthropic")
        print("export GOOGLE_API_KEY=sua_chave_google")
        print("export OPENROUTER_API_KEY=sua_chave_openrouter")

def main():
    """Função principal"""
    print("🚀 Exemplos de Modelos Agno Framework")
    print("=" * 50)
    
    # Verificar configuração
    verificar_configuracao()
    
    # Testar cada provedor
    exemplo_openai()
    exemplo_anthropic()
    exemplo_google_gemini()
    exemplo_openrouter()
    
    # Comparar modelos
    exemplo_comparacao_modelos()
    
    print("\n" + "=" * 50)
    print("🎉 Testes concluídos!")
    print("\n📚 **Recursos Úteis:**")
    print("- Documentação Agno: https://docs.agno.com")
    print("- Modelos OpenRouter: https://openrouter.ai/models")
    print("- Chaves OpenAI: https://platform.openai.com/api-keys")
    print("- Chaves Anthropic: https://console.anthropic.com/")
    print("- Chaves Google: https://makersuite.google.com/app/apikey")
    print("- Chaves OpenRouter: https://openrouter.ai/keys")

if __name__ == "__main__":
    main()