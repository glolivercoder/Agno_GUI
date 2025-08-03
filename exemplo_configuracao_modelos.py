#!/usr/bin/env python3
"""
Exemplo de configuração correta para OpenRouter e Google Gemini
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

def configurar_openrouter():
    """Configura OpenRouter corretamente"""
    print("🌐 Configurando OpenRouter...")
    
    # OpenRouter usa a mesma interface da OpenAI
    # Você pode configurar de duas formas:
    
    # Forma 1: Usando OPENAI_API_KEY (mais comum)
    openrouter_key = os.getenv("OPENROUTER_API_KEY")
    if openrouter_key:
        os.environ["OPENAI_API_KEY"] = openrouter_key
        print("✅ OpenRouter configurado via OPENROUTER_API_KEY")
    
    # Forma 2: Configurar diretamente no código
    # Isso é útil se você quiser usar OpenAI e OpenRouter simultaneamente
    
    # Configurações adicionais do OpenRouter
    os.environ["OPENROUTER_HTTP_REFERER"] = "http://localhost:8501"
    os.environ["OPENROUTER_X_TITLE"] = "Agno Builder"
    
    return bool(openrouter_key)

def exemplo_openrouter_basico():
    """Exemplo básico com OpenRouter"""
    print("\n🚀 Exemplo OpenRouter Básico...")
    
    if not configurar_openrouter():
        print("❌ OPENROUTER_API_KEY não configurada")
        print("💡 Configure no arquivo .env: OPENROUTER_API_KEY=sk-or-v1-sua_chave")
        return False
    
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat  # OpenRouter usa a mesma interface
        
        # Modelo gratuito do OpenRouter
        agent = Agent(
            name="Assistente OpenRouter",
            model=OpenAIChat(
                id="meta-llama/llama-3.1-8b-instruct:free",
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1"
            ),
            instructions=[
                "Você é um assistente usando OpenRouter.",
                "Responda em português de forma útil e concisa."
            ],
            markdown=True,
        )
        
        response = agent.run("Olá! Explique o que é inteligência artificial em 2 frases.")
        print(f"✅ OpenRouter funcionando!")
        print(f"📝 Resposta: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no OpenRouter: {e}")
        return False

def exemplo_openrouter_avancado():
    """Exemplo avançado com OpenRouter usando diferentes modelos"""
    print("\n🎯 Exemplo OpenRouter Avançado...")
    
    if not configurar_openrouter():
        return False
    
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        
        # Lista de modelos para testar
        modelos = [
            {
                "id": "meta-llama/llama-3.1-8b-instruct:free",
                "nome": "Llama 3.1 8B (Gratuito)",
                "gratuito": True
            },
            {
                "id": "openai/gpt-4o-mini",
                "nome": "GPT-4o Mini (Pago)",
                "gratuito": False
            }
        ]
        
        for modelo in modelos:
            print(f"\n🧪 Testando {modelo['nome']}...")
            
            try:
                agent = Agent(
                    name=f"Assistente {modelo['nome']}",
                    model=OpenAIChat(
                        id=modelo["id"],
                        api_key=os.getenv("OPENROUTER_API_KEY"),
                        base_url="https://openrouter.ai/api/v1"
                    ),
                    instructions=[
                        f"Você está usando {modelo['nome']} via OpenRouter.",
                        "Seja conciso e útil."
                    ],
                    markdown=True,
                )
                
                response = agent.run("Qual é a capital do Brasil?")
                print(f"✅ {modelo['nome']}: {response.content[:50]}...")
                
                if modelo["gratuito"]:
                    print("💚 Modelo gratuito!")
                else:
                    print("💰 Modelo pago - verifique custos")
                    
            except Exception as e:
                print(f"❌ Erro com {modelo['nome']}: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def exemplo_google_gemini():
    """Exemplo com Google Gemini"""
    print("\n🔴 Exemplo Google Gemini...")
    
    google_key = os.getenv("GOOGLE_API_KEY")
    if not google_key:
        print("❌ GOOGLE_API_KEY não configurada")
        print("💡 Configure no arquivo .env: GOOGLE_API_KEY=sua_chave_google")
        return False
    
    try:
        from agno.agent import Agent
        from agno.models.google import Gemini
        
        # Criar agente com Gemini
        agent = Agent(
            name="Assistente Gemini",
            model=Gemini(
                id="gemini-2.0-flash-001",
                api_key=google_key
            ),
            instructions=[
                "Você é um assistente usando Google Gemini.",
                "Seja informativo e preciso.",
                "Responda em português."
            ],
            markdown=True,
        )
        
        response = agent.run("Explique machine learning em termos simples.")
        print(f"✅ Gemini funcionando!")
        print(f"📝 Resposta: {response.content}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no Gemini: {e}")
        return False

def exemplo_comparacao():
    """Compara respostas dos diferentes modelos"""
    print("\n🔄 Comparando Modelos...")
    
    pergunta = "O que é inteligência artificial?"
    
    # Testar OpenRouter
    print("\n🌐 OpenRouter:")
    if configurar_openrouter():
        try:
            from agno.agent import Agent
            from agno.models.openai import OpenAIChat
            
            agent_or = Agent(
                model=OpenAIChat(
                    id="meta-llama/llama-3.1-8b-instruct:free",
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                    base_url="https://openrouter.ai/api/v1"
                ),
                instructions=["Seja conciso."]
            )
            
            response = agent_or.run(pergunta)
            print(f"📝 {response.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Erro: {e}")
    
    # Testar Gemini
    print("\n🔴 Google Gemini:")
    if os.getenv("GOOGLE_API_KEY"):
        try:
            from agno.agent import Agent
            from agno.models.google import Gemini
            
            agent_gemini = Agent(
                model=Gemini(id="gemini-2.0-flash-001"),
                instructions=["Seja conciso."]
            )
            
            response = agent_gemini.run(pergunta)
            print(f"📝 {response.content[:100]}...")
            
        except Exception as e:
            print(f"❌ Erro: {e}")

def mostrar_configuracao():
    """Mostra como configurar as chaves de API"""
    print("🔧 Como Configurar as APIs:")
    print("=" * 50)
    
    print("\n1️⃣ Google Gemini:")
    print("   • Acesse: https://makersuite.google.com/app/apikey")
    print("   • Crie uma chave de API")
    print("   • Adicione no .env: GOOGLE_API_KEY=sua_chave")
    
    print("\n2️⃣ OpenRouter:")
    print("   • Acesse: https://openrouter.ai/keys")
    print("   • Crie uma conta e gere uma chave")
    print("   • Adicione no .env: OPENROUTER_API_KEY=sk-or-v1-sua_chave")
    
    print("\n3️⃣ Arquivo .env exemplo:")
    print("   GOOGLE_API_KEY=AIzaSy...")
    print("   OPENROUTER_API_KEY=sk-or-v1-...")
    print("   PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python")
    
    print("\n💡 Dicas:")
    print("   • OpenRouter tem modelos gratuitos!")
    print("   • Gemini tem cota gratuita generosa")
    print("   • Sempre verifique os custos antes de usar modelos pagos")

def main():
    """Função principal"""
    print("🤖 Configuração OpenRouter e Google Gemini")
    print("=" * 60)
    
    # Mostrar como configurar
    mostrar_configuracao()
    
    print("\n" + "=" * 60)
    print("🧪 Testando Configurações...")
    
    # Testar cada provedor
    openrouter_ok = exemplo_openrouter_basico()
    gemini_ok = exemplo_google_gemini()
    
    if openrouter_ok:
        exemplo_openrouter_avancado()
    
    if openrouter_ok or gemini_ok:
        exemplo_comparacao()
    
    # Resumo final
    print("\n" + "=" * 60)
    print("📊 Resumo:")
    print(f"   🌐 OpenRouter: {'✅ OK' if openrouter_ok else '❌ Falhou'}")
    print(f"   🔴 Google Gemini: {'✅ OK' if gemini_ok else '❌ Falhou'}")
    
    if openrouter_ok or gemini_ok:
        print("\n🎉 Pelo menos um provedor está funcionando!")
        print("💡 Agora você pode usar o Agno Builder normalmente")
    else:
        print("\n⚠️ Nenhum provedor configurado")
        print("💡 Configure suas chaves de API no arquivo .env")

if __name__ == "__main__":
    main()