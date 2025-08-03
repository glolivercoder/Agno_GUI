#!/usr/bin/env python3
"""
Teste simples APENAS para OpenRouter
"""

import os
from dotenv import load_dotenv

# Carregar .env
load_dotenv()

# Configurar protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

def testar_openrouter():
    """Testa APENAS OpenRouter"""
    print("🌐 Testando OpenRouter...")
    
    # Verificar se a chave está configurada
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        print("❌ OPENAI_API_KEY não configurada")
        print("💡 Para usar OpenRouter:")
        print("   1. Vá para: https://openrouter.ai/keys")
        print("   2. Crie uma conta e gere uma chave")
        print("   3. Edite o arquivo .env:")
        print("   4. Coloque: OPENAI_API_KEY=sk-or-v1-sua_chave_aqui")
        return False
    
    if not openai_key.startswith("sk-or-"):
        print("⚠️ A chave não parece ser do OpenRouter")
        print("💡 Chaves do OpenRouter começam com 'sk-or-v1-'")
        print(f"   Sua chave atual: {openai_key[:10]}...")
    
    try:
        from agno.agent import Agent
        from agno.models.openrouter import OpenRouter
        
        print("✅ Importações OK")
        
        # Testar modelo gratuito
        print("🆓 Testando modelo gratuito...")
        agent = Agent(
            name="Teste OpenRouter",
            model=OpenRouter(id="mistralai/mistral-7b-instruct:free"),
            instructions=["Responda em português", "Seja conciso"],
            markdown=True,
        )
        
        print("✅ Agente criado")
        
        # Fazer uma pergunta simples
        response = agent.run("Olá! Diga apenas 'Funcionando' se você conseguir me responder.")
        print(f"✅ OpenRouter funcionando!")
        print(f"📝 Resposta: {response.content}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Teste OpenRouter Simples")
    print("=" * 40)
    
    if testar_openrouter():
        print("\n🎉 OpenRouter está funcionando!")
    else:
        print("\n❌ OpenRouter não está funcionando")
        print("💡 Configure sua chave no arquivo .env")