#!/usr/bin/env python3
"""
Cliente da API OpenRouter para buscar modelos disponíveis
"""

import requests
import time
from typing import List, Dict, Optional
from dataclasses import dataclass
import streamlit as st

@dataclass
class OpenRouterModel:
    """Estrutura de dados para um modelo do OpenRouter"""
    id: str
    name: str
    company: str
    is_free: bool
    price_input: Optional[float] = None
    price_output: Optional[float] = None
    context_length: int = 0
    description: str = ""
    capabilities: List[str] = None

    def __post_init__(self):
        if self.capabilities is None:
            self.capabilities = []

class OpenRouterAPI:
    """Cliente para a API do OpenRouter"""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    TIMEOUT = 10  # segundos
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update({
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "Agno Builder"
            })
    
    def get_models(self) -> List[OpenRouterModel]:
        """
        Busca lista de modelos disponíveis do OpenRouter
        
        Returns:
            Lista de modelos ou lista vazia em caso de erro
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/models",
                timeout=self.TIMEOUT
            )
            
            if response.status_code == 200:
                data = response.json()
                models = []
                
                for model_data in data.get("data", []):
                    try:
                        model = self._parse_model(model_data)
                        if model:
                            models.append(model)
                    except Exception as e:
                        # Log do erro mas continua processando outros modelos
                        print(f"Erro ao processar modelo {model_data.get('id', 'unknown')}: {e}")
                        continue
                
                return models
            
            else:
                print(f"Erro na API OpenRouter: {response.status_code}")
                return self._get_fallback_models()
                
        except requests.exceptions.Timeout:
            print("Timeout na API OpenRouter")
            return self._get_fallback_models()
        except requests.exceptions.RequestException as e:
            print(f"Erro de rede na API OpenRouter: {e}")
            return self._get_fallback_models()
        except Exception as e:
            print(f"Erro inesperado na API OpenRouter: {e}")
            return self._get_fallback_models()
    
    def _parse_model(self, model_data: Dict) -> Optional[OpenRouterModel]:
        """
        Converte dados da API para estrutura OpenRouterModel
        
        Args:
            model_data: Dados do modelo da API
            
        Returns:
            OpenRouterModel ou None se inválido
        """
        try:
            model_id = model_data.get("id", "")
            if not model_id:
                return None
            
            # Extrair empresa do ID (ex: "openai/gpt-4" -> "openai")
            company = model_id.split("/")[0] if "/" in model_id else "unknown"
            
            # Nome amigável
            name = model_data.get("name", model_id)
            
            # Verificar se é gratuito
            pricing = model_data.get("pricing", {})
            prompt_price = float(pricing.get("prompt", "0") or "0")
            completion_price = float(pricing.get("completion", "0") or "0")
            is_free = prompt_price == 0 and completion_price == 0
            
            # Context length
            context_length = model_data.get("context_length", 0)
            
            # Descrição
            description = model_data.get("description", "")
            
            return OpenRouterModel(
                id=model_id,
                name=name,
                company=company.title(),
                is_free=is_free,
                price_input=prompt_price if prompt_price > 0 else None,
                price_output=completion_price if completion_price > 0 else None,
                context_length=context_length,
                description=description,
                capabilities=[]  # Será preenchido se disponível na API
            )
            
        except Exception as e:
            print(f"Erro ao fazer parse do modelo: {e}")
            return None
    
    def _get_fallback_models(self) -> List[OpenRouterModel]:
        """
        Lista de modelos em fallback quando a API não está disponível
        
        Returns:
            Lista de modelos populares
        """
        fallback_models = [
            # Modelos gratuitos
            OpenRouterModel(
                id="mistralai/mistral-7b-instruct:free",
                name="Mistral 7B Instruct",
                company="Mistralai",
                is_free=True,
                context_length=32768,
                description="Modelo gratuito da Mistral AI"
            ),
            OpenRouterModel(
                id="huggingfaceh4/zephyr-7b-beta:free",
                name="Zephyr 7B Beta",
                company="Huggingface",
                is_free=True,
                context_length=32768,
                description="Modelo gratuito do Hugging Face"
            ),
            OpenRouterModel(
                id="openchat/openchat-7b:free",
                name="OpenChat 7B",
                company="Openchat",
                is_free=True,
                context_length=8192,
                description="Modelo de chat gratuito"
            ),
            
            # Modelos pagos populares
            OpenRouterModel(
                id="openai/gpt-4o",
                name="GPT-4o",
                company="Openai",
                is_free=False,
                price_input=0.000005,
                price_output=0.000015,
                context_length=128000,
                description="Modelo mais avançado da OpenAI"
            ),
            OpenRouterModel(
                id="openai/gpt-4o-mini",
                name="GPT-4o Mini",
                company="Openai",
                is_free=False,
                price_input=0.00000015,
                price_output=0.0000006,
                context_length=128000,
                description="Versão mais barata do GPT-4o"
            ),
            OpenRouterModel(
                id="anthropic/claude-3-5-sonnet",
                name="Claude 3.5 Sonnet",
                company="Anthropic",
                is_free=False,
                price_input=0.000003,
                price_output=0.000015,
                context_length=200000,
                description="Modelo avançado da Anthropic"
            ),
            OpenRouterModel(
                id="google/gemini-2.0-flash-exp",
                name="Gemini 2.0 Flash Experimental",
                company="Google",
                is_free=False,
                price_input=0.000001,
                price_output=0.000002,
                context_length=1000000,
                description="Modelo experimental do Google"
            ),
            OpenRouterModel(
                id="meta-llama/llama-3.1-70b-instruct",
                name="Llama 3.1 70B Instruct",
                company="Meta",
                is_free=False,
                price_input=0.00000088,
                price_output=0.00000088,
                context_length=131072,
                description="Modelo grande da Meta"
            )
        ]
        
        return fallback_models

class ModelCache:
    """Sistema de cache para modelos do OpenRouter"""
    
    def __init__(self, cache_duration: int = 3600):  # 1 hora
        self.cache_duration = cache_duration
        self.cache_key = "openrouter_models_cache"
        self.timestamp_key = "openrouter_models_timestamp"
    
    def get_cached_models(self) -> Optional[List[OpenRouterModel]]:
        """
        Recupera modelos do cache se ainda válidos
        
        Returns:
            Lista de modelos ou None se cache inválido
        """
        if self.cache_key not in st.session_state:
            return None
        
        if self.timestamp_key not in st.session_state:
            return None
        
        # Verificar se cache ainda é válido
        cache_time = st.session_state[self.timestamp_key]
        current_time = time.time()
        
        if current_time - cache_time > self.cache_duration:
            # Cache expirado
            return None
        
        return st.session_state[self.cache_key]
    
    def cache_models(self, models: List[OpenRouterModel]) -> None:
        """
        Armazena modelos no cache
        
        Args:
            models: Lista de modelos para cachear
        """
        st.session_state[self.cache_key] = models
        st.session_state[self.timestamp_key] = time.time()
    
    def clear_cache(self) -> None:
        """Remove modelos do cache"""
        if self.cache_key in st.session_state:
            del st.session_state[self.cache_key]
        if self.timestamp_key in st.session_state:
            del st.session_state[self.timestamp_key]

def get_openrouter_models(api_key: Optional[str] = None, use_cache: bool = True) -> List[OpenRouterModel]:
    """
    Função principal para obter modelos do OpenRouter
    
    Args:
        api_key: Chave da API (opcional)
        use_cache: Se deve usar cache
        
    Returns:
        Lista de modelos disponíveis
    """
    cache = ModelCache()
    
    # Tentar usar cache primeiro
    if use_cache:
        cached_models = cache.get_cached_models()
        if cached_models:
            return cached_models
    
    # Buscar da API
    api_client = OpenRouterAPI(api_key)
    models = api_client.get_models()
    
    # Cachear resultado
    if models and use_cache:
        cache.cache_models(models)
    
    return models

# Função de teste
def test_openrouter_api():
    """Testa o cliente da API"""
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")  # OpenRouter usa OPENAI_API_KEY
    
    print("🧪 Testando cliente da API OpenRouter...")
    
    client = OpenRouterAPI(api_key)
    models = client.get_models()
    
    print(f"✅ Encontrados {len(models)} modelos")
    
    # Mostrar alguns exemplos
    free_models = [m for m in models if m.is_free]
    paid_models = [m for m in models if not m.is_free]
    
    print(f"🆓 Modelos gratuitos: {len(free_models)}")
    print(f"💰 Modelos pagos: {len(paid_models)}")
    
    # Mostrar empresas
    companies = set(m.company for m in models)
    print(f"🏢 Empresas: {', '.join(sorted(companies))}")
    
    # Mostrar alguns modelos gratuitos
    print("\n🆓 Alguns modelos gratuitos:")
    for model in free_models[:3]:
        print(f"   • {model.name} ({model.id})")
    
    # Mostrar alguns modelos pagos
    print("\n💰 Alguns modelos pagos:")
    for model in paid_models[:3]:
        price_info = ""
        if model.price_input:
            price_info = f" - ${model.price_input:.6f}/token"
        print(f"   • {model.name} ({model.id}){price_info}")

if __name__ == "__main__":
    test_openrouter_api()