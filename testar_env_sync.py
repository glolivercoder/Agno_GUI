#!/usr/bin/env python3
"""
Teste para verificar sincronização entre .env e interface
"""

import os
from pathlib import Path

def test_env_loading():
    """Testa carregamento do arquivo .env"""
    print("🧪 Testando carregamento do arquivo .env...")
    
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ Arquivo .env não encontrado")
        return False
    
    print("✅ Arquivo .env encontrado")
    
    # Ler arquivo .env
    env_vars = {}
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    env_vars[key] = value
                    print(f"  Linha {line_num}: {key} = {value[:10]}..." if len(value) > 10 else f"  Linha {line_num}: {key} = {value}")
    except Exception as e:
        print(f"❌ Erro ao ler .env: {e}")
        return False
    
    print(f"\n📊 Variáveis encontradas: {len(env_vars)}")
    
    # Verificar chaves de API específicas
    api_keys = ['OPENAI_API_KEY', 'ANTHROPIC_API_KEY', 'GOOGLE_API_KEY', 'OPENROUTER_API_KEY']
    
    print("\n🔑 Status das chaves de API:")
    for key in api_keys:
        value = env_vars.get(key, '')
        if value:
            print(f"  ✅ {key}: {value[:8]}...{value[-4:]}" if len(value) > 12 else f"  ✅ {key}: ***")
        else:
            print(f"  ❌ {key}: Não configurado")
    
    # Verificar se as variáveis estão no os.environ
    print("\n🌍 Status no os.environ:")
    for key in api_keys:
        env_value = os.getenv(key, '')
        if env_value:
            print(f"  ✅ {key}: Disponível no ambiente")
        else:
            print(f"  ❌ {key}: Não disponível no ambiente")
    
    return True

def test_agno_detection():
    """Testa detecção do provedor preferido"""
    print("\n🤖 Testando detecção de provedor...")
    
    # Simular lógica de detecção
    preferred_provider = "OpenRouter"
    preferred_model = "mistralai/mistral-7b-instruct:free"
    
    if os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"):
        preferred_provider = "OpenRouter"
        preferred_model = "mistralai/mistral-7b-instruct:free"
        print(f"  🌐 Detectado: {preferred_provider} com {preferred_model}")
    elif os.getenv("GOOGLE_API_KEY"):
        preferred_provider = "Google Gemini"
        preferred_model = "gemini-2.0-flash-001"
        print(f"  🔴 Detectado: {preferred_provider} com {preferred_model}")
    elif os.getenv("ANTHROPIC_API_KEY"):
        preferred_provider = "Anthropic"
        preferred_model = "claude-3-haiku"
        print(f"  🟠 Detectado: {preferred_provider} com {preferred_model}")
    else:
        print("  ❌ Nenhum provedor detectado")
        return False
    
    return True

def test_agno_import():
    """Testa importação do Agno"""
    print("\n📦 Testando importação do Agno...")
    
    try:
        import agno
        print("  ✅ agno importado com sucesso")
        
        from agno.agent import Agent
        print("  ✅ Agent importado com sucesso")
        
        from agno.models.openai import OpenAIChat
        print("  ✅ OpenAIChat importado com sucesso")
        
        try:
            from agno.models.google import Gemini
            print("  ✅ Gemini importado com sucesso")
        except ImportError:
            print("  ⚠️ Gemini não disponível")
        
        try:
            from agno.models.anthropic import Claude
            print("  ✅ Claude importado com sucesso")
        except ImportError:
            print("  ⚠️ Claude não disponível")
        
        try:
            from agno.models.openrouter import OpenRouter
            print("  ✅ OpenRouter importado com sucesso")
        except ImportError:
            print("  ⚠️ OpenRouter não disponível")
        
        return True
        
    except ImportError as e:
        print(f"  ❌ Erro ao importar Agno: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🔧 Teste de Sincronização .env ↔ Interface")
    print("=" * 50)
    
    # Configurar protobuf
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    
    # Carregar .env manualmente
    env_path = Path(".env")
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    if value and not value.startswith('xxx'):
                        os.environ[key] = value
    
    # Executar testes
    tests = [
        ("Carregamento do .env", test_env_loading),
        ("Detecção de provedor", test_agno_detection),
        ("Importação do Agno", test_agno_import)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste '{test_name}': {e}")
            results.append((test_name, False))
    
    # Resumo
    print("\n" + "=" * 50)
    print("📊 Resumo dos Testes:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Resultado: {passed}/{len(results)} testes passaram")
    
    if passed == len(results):
        print("🎉 Todos os testes passaram! A sincronização deve funcionar.")
    else:
        print("⚠️ Alguns testes falharam. Verifique a configuração.")

if __name__ == "__main__":
    main()