#!/usr/bin/env python3
"""
Teste do sistema de cache e fallback do OpenRouter
"""

import time
import streamlit as st
from openrouter_api import ModelCache, OpenRouterAPI, get_openrouter_models

def test_cache_system():
    """Testa o sistema de cache"""
    print("🧪 Testando sistema de cache...")
    
    # Simular session state do Streamlit
    if not hasattr(st, 'session_state'):
        st.session_state = {}
    
    cache = ModelCache(cache_duration=5)  # 5 segundos para teste
    
    # Teste 1: Cache vazio
    cached = cache.get_cached_models()
    assert cached is None, "Cache deveria estar vazio inicialmente"
    print("✅ Cache vazio funcionando")
    
    # Teste 2: Adicionar ao cache
    from openrouter_api import OpenRouterModel
    test_models = [
        OpenRouterModel(
            id="test/model",
            name="Test Model",
            company="Test",
            is_free=True
        )
    ]
    
    cache.cache_models(test_models)
    cached = cache.get_cached_models()
    assert cached is not None, "Cache deveria ter modelos"
    assert len(cached) == 1, "Cache deveria ter 1 modelo"
    assert cached[0].id == "test/model", "Modelo incorreto no cache"
    print("✅ Cache armazenamento funcionando")
    
    # Teste 3: Cache ainda válido
    cached_again = cache.get_cached_models()
    assert cached_again is not None, "Cache ainda deveria ser válido"
    print("✅ Cache TTL funcionando")
    
    # Teste 4: Cache expirado
    print("⏳ Aguardando cache expirar...")
    time.sleep(6)  # Esperar cache expirar
    expired = cache.get_cached_models()
    assert expired is None, "Cache deveria ter expirado"
    print("✅ Cache expiração funcionando")
    
    # Teste 5: Limpar cache
    cache.cache_models(test_models)
    cache.clear_cache()
    cleared = cache.get_cached_models()
    assert cleared is None, "Cache deveria estar limpo"
    print("✅ Cache limpeza funcionando")

def test_fallback_system():
    """Testa o sistema de fallback"""
    print("\n🧪 Testando sistema de fallback...")
    
    # Criar cliente sem API key para forçar fallback
    client = OpenRouterAPI(api_key=None)
    
    # Simular erro de rede modificando a URL
    client.BASE_URL = "https://url-inexistente.com"
    
    models = client.get_models()
    
    assert len(models) > 0, "Fallback deveria retornar modelos"
    
    # Verificar se tem modelos gratuitos e pagos
    free_models = [m for m in models if m.is_free]
    paid_models = [m for m in models if not m.is_free]
    
    assert len(free_models) > 0, "Fallback deveria ter modelos gratuitos"
    assert len(paid_models) > 0, "Fallback deveria ter modelos pagos"
    
    print(f"✅ Fallback retornou {len(models)} modelos")
    print(f"   🆓 Gratuitos: {len(free_models)}")
    print(f"   💰 Pagos: {len(paid_models)}")
    
    # Verificar empresas
    companies = set(m.company for m in models)
    expected_companies = {"Mistralai", "Huggingface", "Openchat", "Openai", "Anthropic", "Google", "Meta"}
    
    assert len(companies.intersection(expected_companies)) > 0, "Fallback deveria ter empresas conhecidas"
    print(f"✅ Empresas no fallback: {', '.join(sorted(companies))}")

def test_integration():
    """Testa integração completa"""
    print("\n🧪 Testando integração completa...")
    
    # Simular session state limpo
    if hasattr(st, 'session_state'):
        st.session_state.clear()
    
    # Teste com cache
    models1 = get_openrouter_models(api_key=None, use_cache=True)
    assert len(models1) > 0, "Deveria retornar modelos"
    
    # Teste cache hit
    start_time = time.time()
    models2 = get_openrouter_models(api_key=None, use_cache=True)
    cache_time = time.time() - start_time
    
    assert len(models2) == len(models1), "Cache deveria retornar mesma quantidade"
    assert cache_time < 0.1, f"Cache deveria ser rápido, levou {cache_time:.3f}s"
    
    print(f"✅ Cache hit em {cache_time:.3f}s")
    
    # Teste sem cache
    start_time = time.time()
    models3 = get_openrouter_models(api_key=None, use_cache=False)
    no_cache_time = time.time() - start_time
    
    print(f"✅ Sem cache em {no_cache_time:.3f}s")
    print(f"   Cache é {no_cache_time/cache_time:.1f}x mais rápido")

if __name__ == "__main__":
    print("🚀 Testando Sistema de Cache e Fallback")
    print("=" * 50)
    
    try:
        test_cache_system()
        test_fallback_system()
        test_integration()
        
        print("\n" + "=" * 50)
        print("🎉 Todos os testes passaram!")
        
    except AssertionError as e:
        print(f"\n❌ Teste falhou: {e}")
    except Exception as e:
        print(f"\n💥 Erro inesperado: {e}")
        import traceback
        traceback.print_exc()