# Design Document

## Overview

Esta funcionalidade implementará uma interface avançada para seleção de modelos do OpenRouter no Agno Builder. A solução incluirá busca em tempo real, filtros por empresa e tipo (gratuito/pago), cache inteligente e fallback para garantir disponibilidade.

## Architecture

### Component Structure
```
OpenRouterModelsInterface/
├── components/
│   ├── ModelSelector.py          # Componente principal
│   ├── ModelFilters.py           # Filtros e busca
│   ├── ModelCard.py              # Card individual do modelo
│   └── LoadingState.py           # Estados de carregamento
├── services/
│   ├── OpenRouterAPI.py          # Cliente da API OpenRouter
│   ├── ModelCache.py             # Sistema de cache
│   └── ModelParser.py            # Parser de dados dos modelos
└── utils/
    ├── model_fallback.py         # Lista de fallback
    └── price_formatter.py        # Formatação de preços
```

### Data Flow
1. **Inicialização**: Carrega modelos do cache ou API
2. **Filtros**: Aplica filtros em tempo real nos dados
3. **Seleção**: Retorna modelo selecionado para o componente pai
4. **Cache**: Atualiza cache periodicamente

## Components and Interfaces

### ModelSelector Component
```python
class ModelSelector:
    def __init__(self, api_key: str, cache_duration: int = 3600):
        self.api_client = OpenRouterAPI(api_key)
        self.cache = ModelCache(cache_duration)
        self.models = []
        self.filtered_models = []
    
    def render(self) -> str:
        """Renderiza o seletor completo de modelos"""
        
    def load_models(self) -> List[Model]:
        """Carrega modelos da API ou cache"""
        
    def filter_models(self, filters: Dict) -> List[Model]:
        """Aplica filtros aos modelos"""
```

### ModelFilters Component
```python
class ModelFilters:
    def render_search_box(self) -> None:
        """Renderiza caixa de busca"""
        
    def render_company_dropdown(self, companies: List[str]) -> str:
        """Renderiza dropdown de empresas"""
        
    def render_price_checkboxes(self) -> Tuple[bool, bool]:
        """Renderiza checkboxes gratuito/pago"""
```

### OpenRouterAPI Service
```python
class OpenRouterAPI:
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def get_models(self) -> List[Dict]:
        """Busca lista de modelos da API"""
        
    def get_model_details(self, model_id: str) -> Dict:
        """Busca detalhes específicos de um modelo"""
```

## Data Models

### Model Data Structure
```python
@dataclass
class Model:
    id: str                    # ID único do modelo
    name: str                  # Nome amigável
    company: str               # Empresa (openai, google, etc.)
    is_free: bool             # Se é gratuito
    price_input: Optional[float]   # Preço por token de entrada
    price_output: Optional[float]  # Preço por token de saída
    context_length: int        # Tamanho do contexto
    description: str           # Descrição do modelo
    capabilities: List[str]    # Capacidades (text, vision, etc.)
```

### Filter State
```python
@dataclass
class FilterState:
    search_query: str = ""
    selected_company: str = "Todas"
    show_only_free: bool = False
    show_only_paid: bool = False
```

## Error Handling

### API Failures
- **Timeout**: Fallback para lista cached/estática após 3 segundos
- **Rate Limit**: Exibe mensagem e usa cache existente
- **Network Error**: Usa lista de modelos em fallback
- **Invalid API Key**: Exibe erro específico com instruções

### Data Validation
- Valida estrutura dos dados da API
- Sanitiza inputs de busca
- Verifica consistência dos filtros

### User Experience
- Loading states durante carregamento
- Mensagens de erro amigáveis
- Fallback graceful para funcionalidade básica

## Testing Strategy

### Unit Tests
- `test_model_selector.py`: Testa componente principal
- `test_api_client.py`: Testa cliente da API
- `test_filters.py`: Testa lógica de filtros
- `test_cache.py`: Testa sistema de cache

### Integration Tests
- `test_full_workflow.py`: Testa fluxo completo
- `test_api_integration.py`: Testa integração com API real
- `test_streamlit_integration.py`: Testa integração com Streamlit

### Performance Tests
- Tempo de carregamento < 3 segundos
- Filtros em tempo real < 100ms
- Cache hit ratio > 90%

## Implementation Details

### Streamlit Integration
```python
def render_openrouter_models():
    """Integração com interface Streamlit existente"""
    
    # Estado da sessão
    if 'openrouter_models' not in st.session_state:
        st.session_state.openrouter_models = []
    
    # Componente de seleção
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            search = st.text_input("🔍 Buscar modelo")
        
        with col2:
            company = st.selectbox("🏢 Empresa", companies)
        
        with col3:
            free_only = st.checkbox("🆓 Apenas gratuitos")
            paid_only = st.checkbox("💰 Apenas pagos")
```

### Cache Strategy
- **TTL**: 1 hora para dados da API
- **Storage**: Session state do Streamlit
- **Invalidation**: Manual via botão "Atualizar"
- **Fallback**: Lista estática de modelos populares

### API Rate Limiting
- **Requests**: Máximo 1 request por minuto para lista de modelos
- **Retry**: Exponential backoff em caso de rate limit
- **Circuit Breaker**: Para após 3 falhas consecutivas

## Security Considerations

### API Key Management
- Nunca expor chave da API no frontend
- Validar chave antes de fazer requests
- Usar HTTPS para todas as comunicações

### Input Sanitization
- Sanitizar queries de busca
- Validar seleções de filtros
- Prevenir injection attacks

### Error Information
- Não vazar informações sensíveis em erros
- Logs detalhados apenas no backend
- Mensagens de erro genéricas para usuário