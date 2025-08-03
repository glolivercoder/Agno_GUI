#!/usr/bin/env python3
"""
Script de teste específico para OpenRouter e Google Gemini
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

def teste_google_gemini():
    """Testa Google Gemini"""
    print("🔴 Testando Google Gemini...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ GOOGLE_API_KEY não configurada")
        print("💡 Configure no arquivo .env: GOOGLE_API_KEY=sua_chave")
        return False
    
    try:
        from agno.agent import Agent
        from agno.models.google import Gemini
        
        # Criar agente com Gemini
        agent = Agent(
            name="Assistente Gemini",
            model=Gemini(id="gemini-2.0-flash-001"),
            instructions=[
                "Você é um assistente usando Google Gemini.",
                "Seja conciso e útil.",
                "Responda em português."
            ],
            markdown=True,
        )
        
        # Testar resposta
        response = agent.run("Olá! Explique o que é inteligência artificial em 2 frases.")
        print(f"✅ Gemini funcionando!")
        print(f"📝 Resposta: {response.content[:100]}...")
        return True
        
    except Exception as e:
        print(f"❌ Erro no Gemini: {e}")
        return False

def teste_openrouter():
    """Testa OpenRouter"""
    print("\n🌐 Testando OpenRouter...")
    
    if not os.getenv("OPENROUTER_API_KEY"):
        print("❌ OPENROUTER_API_KEY não configurada")
        print("💡 Configure no arquivo .env: OPENROUTER_API_KEY=sua_chave")
        return False
    
    try:
        from agno.agent import Agent
        from agno.models.openrouter import OpenRouter
        
        # Testar modelo gratuito primeiro
        print("🆓 Testando modelo gratuito...")
        agent_free = Agent(
            name="Assistente OpenRouter Gratuito",
            model=OpenRouter(id="meta-llama/llama-3.1-8b-instruct:free"),
            instructions=[
                "Você é um assistente usando OpenRouter.",
                "Seja útil e eficiente.",
                "Responda em português."
            ],
            markdown=True,
        )
        
        response = agent_free.run("Olá! O que você pode fazer?")
        print(f"✅ OpenRouter (gratuito) funcionando!")
        print(f"📝 Resposta: {response.content[:100]}...")
        
        # Testar modelo premium se disponível
        print("\n💎 Testando modelo premium...")
        agent_premium = Agent(
            name="Assistente OpenRouter Premium",
            model=OpenRouter(id="openai/gpt-4o-mini"),
            instructions=[
                "Você é um assistente premium via OpenRouter.",
                "Forneça respostas de alta qualidade.",
                "Responda em português."
            ],
            markdown=True,
        )
        
        response = agent_premium.run("Explique machine learning brevemente.")
        print(f"✅ OpenRouter (premium) funcionando!")
        print(f"📝 Resposta: {response.content[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no OpenRouter: {e}")
        return False

def listar_modelos_openrouter():
    """Lista modelos populares do OpenRouter"""
    print("\n📋 Modelos OpenRouter Populares:")
    
    modelos_gratuitos = [
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "huggingface/zephyr-7b-beta:free"
    ]
    
    modelos_pagos = [
        "openai/gpt-4o",
        "openai/gpt-4o-mini", 
        "anthropic/claude-3-5-sonnet",
        "google/gemini-2.0-flash-exp",
        "meta-llama/llama-3.1-70b-instruct"
    ]
    
    print("\n🆓 Modelos Gratuitos:")
    for modelo in modelos_gratuitos:
        print(f"   • {modelo}")
    
    print("\n💰 Modelos Pagos:")
    for modelo in modelos_pagos:
        print(f"   • {modelo}")
    
    print("\n🔗 Mais modelos: https://openrouter.ai/models")

def verificar_configuracao():
    """Verifica configuração das APIs"""
    print("🔍 Verificando Configuração...")
    
    apis = {
        "Google Gemini": "GOOGLE_API_KEY",
        "OpenRouter": "OPENROUTER_API_KEY"
    }
    
    configuradas = []
    nao_configuradas = []
    
    for nome, var in apis.items():
        if os.getenv(var):
            configuradas.append(f"✅ {nome}")
        else:
            nao_configuradas.append(f"❌ {nome}")
    
    if configuradas:
        print("\nAPIs Configuradas:")
        for api in configuradas:
            print(f"  {api}")
    
    if nao_configuradas:
        print("\nAPIs Não Configuradas:")
        for api in nao_configuradas:
            print(f"  {api}")
        
        print("\n💡 Para configurar:")
        print("1. Edite o arquivo .env")
        print("2. Adicione suas chaves:")
        print("   GOOGLE_API_KEY=sua_chave_google")
        print("   OPENROUTER_API_KEY=sua_chave_openrouter")
        
        print("\n🔗 Obter chaves:")
        print("   Google: https://makersuite.google.com/app/apikey")
        print("   OpenRouter: https://openrouter.ai/keys")

def main():
    """Função principal"""
    print("🧪 Teste OpenRouter e Google Gemini")
    print("=" * 50)
    
    # Verificar configuração
    verificar_configuracao()
    
    # Listar modelos
    listar_modelos_openrouter()
    
    print("\n" + "=" * 50)
    print("🚀 Iniciando Testes...")
    
    # Testar APIs
    gemini_ok = teste_google_gemini()
    openrouter_ok = teste_openrouter()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 Resumo dos Testes:")
    print(f"   🔴 Google Gemini: {'✅ OK' if gemini_ok else '❌ Falhou'}")
    print(f"   🌐 OpenRouter: {'✅ OK' if openrouter_ok else '❌ Falhou'}")
    
    if gemini_ok or openrouter_ok:
        print("\n🎉 Pelo menos um provedor está funcionando!")
        print("💡 Agora você pode usar a interface do Agno Builder")
    else:
        print("\n⚠️ Nenhum provedor funcionou")
        print("💡 Verifique suas chaves de API no arquivo .env")

if __name__ == "__main__":
    main()