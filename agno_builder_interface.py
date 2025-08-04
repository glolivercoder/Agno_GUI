#!/usr/bin/env python3
"""
Agno Agent Builder - Interface Gráfica para Criação de Agentes
Implementação completa de uma interface visual para criar agentes Agno por níveis
"""

import streamlit as st
import json
import yaml
from typing import Dict, List, Any, Optional
from datetime import datetime
import os

# Configurar protobuf antes dos imports
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Imports do Agno
try:
    import sys
    import subprocess
    
    # Verificar se estamos no ambiente virtual correto
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # Estamos em um ambiente virtual
        try:
            from agno.agent import Agent
            from agno.models.openai import OpenAIChat
            from agno.models.anthropic import Claude
            from agno.models.openrouter import OpenRouter
            from agno.models.google import Gemini
            from agno.playground import Playground
            from agno.tools.duckduckgo import DuckDuckGoTools
            from agno.tools.calculator import CalculatorTools
            from agno.tools.yfinance import YFinanceTools
            from agno.team import Team
            from agno.workflow import Workflow
            AGNO_AVAILABLE = True
        except ImportError as e:
            AGNO_AVAILABLE = False
            st.error(f"❌ Erro ao importar Agno: {e}")
            st.info("💡 Execute no ambiente virtual: .venv\\Scripts\\activate")
    else:
        AGNO_AVAILABLE = False
        st.warning("⚠️ Ambiente virtual não detectado. Ative o ambiente virtual primeiro.")
        st.code(".venv\\Scripts\\activate  # Windows")
        st.code("source .venv/bin/activate  # Linux/Mac")
        
except Exception as e:
    AGNO_AVAILABLE = False
    st.error(f"❌ Erro inesperado: {e}")

class AgnoAgentBuilder:
    """
    Interface gráfica completa para criação de agentes Agno
    Suporta os 5 níveis de sistemas agênticos com assistência de IA
    """
    
    def __init__(self):
        self.config = {}
        self.generated_code = ""
    
    def create_ai_assistant(self):
        """Cria assistente IA especializado em Agno"""
        if not AGNO_AVAILABLE:
            return None
            
        return Agent(
            name="Agno Builder Assistant",
            model=OpenAIChat(id="gpt-4"),
            tools=[DuckDuckGoTools(), CalculatorTools()],
            instructions=[
                "Você é um especialista em Agno Framework.",
                "Ajude usuários a criar agentes otimizados para cada nível.",
                "Sugira ferramentas, configurações e melhores práticas.",
                "Explique conceitos técnicos de forma clara.",
                "Sempre considere performance e escalabilidade.",
                "Forneça exemplos práticos e funcionais.",
                "Conheça todos os provedores: OpenAI, Anthropic, Google Gemini, OpenRouter.",
                "Para OpenRouter, sugira modelos gratuitos quando apropriado."
            ],
            markdown=True
        )
    
    def get_openrouter_models(self):
        """Obtém lista de modelos OpenRouter populares"""
        return {
            "Populares": [
                {"id": "openai/gpt-4o", "name": "GPT-4o (OpenAI)", "free": False},
                {"id": "anthropic/claude-3-5-sonnet", "name": "Claude 3.5 Sonnet", "free": False},
                {"id": "google/gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash", "free": False},
                {"id": "meta-llama/llama-3.1-8b-instruct:free", "name": "Llama 3.1 8B", "free": True},
                {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B", "free": True}
            ],
            "Gratuitos": [
                {"id": "meta-llama/llama-3.1-8b-instruct:free", "name": "Llama 3.1 8B Instruct", "free": True},
                {"id": "mistralai/mistral-7b-instruct:free", "name": "Mistral 7B Instruct", "free": True},
                {"id": "huggingface/zephyr-7b-beta:free", "name": "Zephyr 7B Beta", "free": True},
                {"id": "openchat/openchat-7b:free", "name": "OpenChat 7B", "free": True},
                {"id": "gryphe/mythomist-7b:free", "name": "MythoMist 7B", "free": True}
            ],
            "OpenAI": [
                {"id": "openai/gpt-4o", "name": "GPT-4o", "free": False},
                {"id": "openai/gpt-4-turbo", "name": "GPT-4 Turbo", "free": False},
                {"id": "openai/gpt-4o-mini", "name": "GPT-4o Mini", "free": False},
                {"id": "openai/gpt-3.5-turbo", "name": "GPT-3.5 Turbo", "free": False}
            ],
            "Anthropic": [
                {"id": "anthropic/claude-3-5-sonnet", "name": "Claude 3.5 Sonnet", "free": False},
                {"id": "anthropic/claude-3-opus", "name": "Claude 3 Opus", "free": False},
                {"id": "anthropic/claude-3-haiku", "name": "Claude 3 Haiku", "free": False}
            ],
            "Google": [
                {"id": "google/gemini-2.0-flash-exp", "name": "Gemini 2.0 Flash Experimental", "free": False},
                {"id": "google/gemini-pro", "name": "Gemini Pro", "free": False},
                {"id": "google/gemini-flash-1.5", "name": "Gemini Flash 1.5", "free": False}
            ]
        }
    
    def render_sidebar(self):
        """Renderiza barra lateral com navegação"""
        st.sidebar.title("🤖 Agno Builder")
        st.sidebar.markdown("### Navegação")
        
        # Seletor de nível
        levels = {
            1: "🛠️ Ferramentas & Instruções",
            2: "📚 Conhecimento & RAG", 
            3: "🧠 Memória & Raciocínio",
            4: "👥 Times de Agentes",
            5: "🔄 Workflows Agênticos"
        }
        
        selected_level = st.sidebar.selectbox(
            "Selecione o Nível:",
            options=list(levels.keys()),
            format_func=lambda x: f"Nível {x}: {levels[x]}",
            index=st.session_state.current_level - 1
        )
        
        st.session_state.current_level = selected_level
        
        # Informações do nível atual
        st.sidebar.markdown("---")
        st.sidebar.markdown("### ℹ️ Sobre este Nível")
        
        level_info = {
            1: "Agentes básicos com ferramentas específicas e instruções personalizadas.",
            2: "Agentes com base de conhecimento (RAG) para consultar documentos e informações.",
            3: "Agentes com memória persistente e capacidade de raciocínio avançado.",
            4: "Múltiplos agentes trabalhando em equipe com diferentes modos de colaboração.",
            5: "Fluxos de trabalho complexos com estado, condições e controle de execução."
        }
        
        st.sidebar.info(level_info[selected_level])
        
        # Informações sobre provedores
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🤖 Provedores Suportados")
        
        providers_info = {
            "OpenAI": {"icon": "🔵", "models": "GPT-4, GPT-3.5", "cost": "Pago"},
            "Anthropic": {"icon": "🟠", "models": "Claude 3.5", "cost": "Pago"},
            "Google Gemini": {"icon": "🔴", "models": "Gemini 2.0", "cost": "Pago"},
            "OpenRouter": {"icon": "🌐", "models": "100+ modelos", "cost": "Varia"},
        }
        
        for provider, info in providers_info.items():
            st.sidebar.markdown(f"""
            **{info['icon']} {provider}**
            - Modelos: {info['models']}
            - Custo: {info['cost']}
            """)
        
        if st.sidebar.button("🔗 Links Úteis"):
            st.sidebar.markdown("""
            **Obter Chaves de API:**
            - [OpenAI](https://platform.openai.com/api-keys)
            - [Anthropic](https://console.anthropic.com/)
            - [Google AI](https://makersuite.google.com/app/apikey)
            - [OpenRouter](https://openrouter.ai/keys)
            
            **Documentação:**
            - [Agno Docs](https://docs.agno.com)
            - [OpenRouter Models](https://openrouter.ai/models)
            """)
        
        # Ações rápidas
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 🚀 Ações Rápidas")
        
        if st.sidebar.button("💡 Obter Sugestões IA"):
            self.get_ai_suggestions(selected_level)
        
        if st.sidebar.button("📋 Carregar Template"):
            self.load_template(selected_level)
        
        if st.sidebar.button("💾 Salvar Configuração"):
            self.save_configuration()
        
        if st.sidebar.button("📤 Exportar Código"):
            self.export_code()
        
        return selected_level
    
    def render_header(self, level: int):
        """Renderiza cabeçalho da página"""
        level_titles = {
            1: "🛠️ Nível 1: Agentes com Ferramentas",
            2: "📚 Nível 2: Agentes com Conhecimento",
            3: "🧠 Nível 3: Agentes com Memória",
            4: "👥 Nível 4: Times de Agentes",
            5: "🔄 Nível 5: Workflows Agênticos"
        }
        
        st.title(level_titles[level])
        
        # Barra de progresso
        progress = level / 5
        st.progress(progress)
        st.markdown(f"**Progresso:** Nível {level} de 5")
        
        st.markdown("---")
    
    def render_level_1_builder(self):
        """Builder para Nível 1: Agentes com ferramentas"""
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("⚙️ Configurações Básicas")
            
            # Configurações do agente
            agent_name = st.text_input(
                "Nome do Agente:",
                value="Meu Assistente",
                help="Nome identificador do seu agente"
            )
            
            agent_role = st.text_input(
                "Função/Papel:",
                value="Assistente especializado",
                help="Descreva o papel principal do agente"
            )
            
            # Seleção do modelo
            col_model1, col_model2 = st.columns(2)
            
            with col_model1:
                model_provider = st.selectbox(
                    "Provedor do Modelo:",
                    ["OpenAI", "Anthropic", "Google Gemini", "OpenRouter", "Groq", "Ollama"],
                    help="Escolha o provedor de IA"
                )
            
            with col_model2:
                if model_provider == "OpenAI":
                    model_id = st.selectbox(
                        "Modelo:",
                        ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o", "gpt-4o-mini"]
                    )
                elif model_provider == "Anthropic":
                    model_id = st.selectbox(
                        "Modelo:",
                        ["claude-3-opus", "claude-3-sonnet", "claude-3-haiku", "claude-3-5-sonnet"]
                    )
                elif model_provider == "Google Gemini":
                    model_id = st.selectbox(
                        "Modelo:",
                        ["gemini-2.0-flash-001", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"]
                    )
                elif model_provider == "OpenRouter":
                    # Nova interface avançada para OpenRouter
                    from openrouter_filters import OpenRouterFilters
                    
                    # Inicializar componente de filtros
                    if 'openrouter_filters' not in st.session_state:
                        st.session_state.openrouter_filters = OpenRouterFilters()
                    
                    # Obter chave da API
                    api_key = os.getenv("OPENAI_API_KEY")
                    
                    # Renderizar interface completa
                    model_id = st.session_state.openrouter_filters.render_complete_interface(api_key)
                    
                    # Fallback para entrada manual se necessário
                    if model_id is None:
                        st.markdown("---")
                        st.markdown("**🔧 Entrada Manual (Opcional)**")
                        model_id = st.text_input(
                            "ID do Modelo OpenRouter:",
                            "mistralai/mistral-7b-instruct:free",
                            help="Digite o ID completo do modelo (ex: openai/gpt-4o)"
                        )
                        st.info("💡 Encontre mais modelos em: https://openrouter.ai/models")
                else:
                    model_id = st.text_input("ID do Modelo:", "modelo-padrao")
            
            # Instruções
            instructions = st.text_area(
                "Instruções do Agente:",
                value="Você é um assistente útil e especializado.\nSempre seja claro e preciso nas respostas.\nUse as ferramentas disponíveis quando necessário.",
                height=120,
                help="Defina como o agente deve se comportar"
            )
            
            # Configurações de API
            with st.expander("�  Configurações de API"):
                st.markdown("**Chaves de API necessárias:**")
                
                if model_provider == "OpenAI":
                    st.code("export OPENAI_API_KEY=sua_chave_openai")
                elif model_provider == "Anthropic":
                    st.code("export ANTHROPIC_API_KEY=sua_chave_anthropic")
                elif model_provider == "Google Gemini":
                    st.code("export GOOGLE_API_KEY=sua_chave_google")
                    st.info("💡 Para Vertex AI: export GOOGLE_GENAI_USE_VERTEXAI=true")
                elif model_provider == "OpenRouter":
                    st.code("export OPENROUTER_API_KEY=sua_chave_openrouter")
                    st.info("💡 Obtenha sua chave em: https://openrouter.ai/keys")
                    
                    # Mostrar preços estimados para OpenRouter
                    if "free" not in model_id.lower():
                        st.warning("⚠️ Este modelo tem custo. Verifique preços em: https://openrouter.ai/models")
                    else:
                        st.success("✅ Modelo gratuito selecionado!")
            
            # Configurações avançadas
            with st.expander("🔧 Configurações Avançadas"):
                show_tool_calls = st.checkbox("Mostrar chamadas de ferramentas", value=True)
                markdown_output = st.checkbox("Saída em Markdown", value=True)
                stream_response = st.checkbox("Resposta em streaming", value=True)
                
                # Configurações específicas do OpenRouter
                if model_provider == "OpenRouter":
                    st.markdown("**Configurações OpenRouter:**")
                    site_url = st.text_input("Site URL:", "http://localhost:8501")
                    site_name = st.text_input("Nome do Site:", "Agno Builder")
        
        with col2:
            st.subheader("🛠️ Ferramentas Disponíveis")
            
            # Categorias de ferramentas
            tools_categories = {
                "🔍 Busca": {
                    "DuckDuckGo": {"class": "DuckDuckGoTools", "import": "agno.tools.duckduckgo"},
                    "Google Search": {"class": "GoogleSearchTools", "import": "agno.tools.googlesearch"},
                    "Exa": {"class": "ExaTools", "import": "agno.tools.exa"},
                    "Tavily": {"class": "TavilyTools", "import": "agno.tools.tavily"}
                },
                "🧮 Cálculos": {
                    "Calculator": {"class": "CalculatorTools", "import": "agno.tools.calculator"},
                    "Pandas": {"class": "PandasTools", "import": "agno.tools.pandas"},
                    "NumPy": {"class": "NumpyTools", "import": "agno.tools.numpy"}
                },
                "🌐 Web": {
                    "Firecrawl": {"class": "FirecrawlTools", "import": "agno.tools.firecrawl"},
                    "Newspaper4k": {"class": "Newspaper4kTools", "import": "agno.tools.newspaper4k"},
                    "BeautifulSoup": {"class": "WebTools", "import": "agno.tools.web"}
                },
                "💰 Financeiro": {
                    "YFinance": {"class": "YFinanceTools", "import": "agno.tools.yfinance"},
                    "OpenBB": {"class": "OpenBBTools", "import": "agno.tools.openbb"},
                    "Alpha Vantage": {"class": "AlphaVantageTools", "import": "agno.tools.alphavantage"}
                },
                "💬 Social": {
                    "Email": {"class": "EmailTools", "import": "agno.tools.email"},
                    "Slack": {"class": "SlackTools", "import": "agno.tools.slack"},
                    "Discord": {"class": "DiscordTools", "import": "agno.tools.discord"},
                    "WhatsApp": {"class": "WhatsAppTools", "import": "agno.tools.whatsapp"}
                },
                "⚙️ Desenvolvimento": {
                    "GitHub": {"class": "GitHubTools", "import": "agno.tools.github"},
                    "Docker": {"class": "DockerTools", "import": "agno.tools.docker"},
                    "Shell": {"class": "ShellTools", "import": "agno.tools.shell"},
                    "Python": {"class": "PythonTools", "import": "agno.tools.python"}
                }
            }
            
            selected_tools = []
            for category, tools in tools_categories.items():
                st.write(f"**{category}**")
                for tool_name, tool_info in tools.items():
                    if st.checkbox(tool_name, key=f"tool_{tool_name}"):
                        selected_tools.append({
                            "name": tool_name,
                            "class": tool_info["class"],
                            "import": tool_info["import"]
                        })
        
        # Salvar configuração no estado
        st.session_state.agent_configs['level_1'] = {
            "name": agent_name,
            "role": agent_role,
            "model_provider": model_provider,
            "model_id": model_id,
            "instructions": instructions,
            "tools": selected_tools,
            "show_tool_calls": show_tool_calls,
            "markdown": markdown_output,
            "stream": stream_response
        }
        
        # Preview do código
        st.markdown("---")
        st.subheader("👀 Preview do Código")
        
        if st.button("🔄 Gerar Código"):
            code = self.generate_level_1_code(st.session_state.agent_configs['level_1'])
            st.code(code, language="python")
            st.session_state.generated_code = code
    
    def render_level_2_builder(self):
        """Builder para Nível 2: Agentes com conhecimento"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📚 Base de Conhecimento")
            
            knowledge_type = st.selectbox(
                "Tipo de Conhecimento:",
                ["Documentos de Texto", "PDFs", "Websites", "CSV/JSON", "YouTube", "ArXiv Papers"]
            )
            
            if knowledge_type == "Documentos de Texto":
                knowledge_path = st.text_input("Caminho dos Documentos:", "documentos/")
                file_formats = st.multiselect(
                    "Formatos de Arquivo:",
                    [".txt", ".md", ".json", ".csv"],
                    default=[".txt", ".md"]
                )
                
            elif knowledge_type == "PDFs":
                knowledge_path = st.text_input("Caminho dos PDFs:", "pdfs/")
                
            elif knowledge_type == "Websites":
                urls_text = st.text_area(
                    "URLs (uma por linha):",
                    "https://docs.agno.com\nhttps://python.org/docs"
                )
                urls_list = [url.strip() for url in urls_text.split('\n') if url.strip()]
                
            elif knowledge_type == "YouTube":
                youtube_urls = st.text_area("URLs do YouTube:", "")
                
            # Configurações de chunking
            st.subheader("✂️ Configurações de Chunking")
            chunk_size = st.slider("Tamanho do Chunk:", 100, 2000, 1000)
            chunk_overlap = st.slider("Sobreposição:", 0, 500, 200)
        
        with col2:
            st.subheader("🗄️ Banco Vetorial")
            
            vector_db = st.selectbox(
                "Banco Vetorial:",
                ["ChromaDB", "LanceDB", "PgVector", "Qdrant", "Pinecone", "Weaviate"]
            )
            
            if vector_db == "PgVector":
                db_url = st.text_input("URL do PostgreSQL:", "postgresql://user:pass@localhost/db")
            elif vector_db == "Pinecone":
                pinecone_api_key = st.text_input("Pinecone API Key:", type="password")
                pinecone_env = st.text_input("Pinecone Environment:", "us-west1-gcp")
            
            # Configurações de embeddings
            st.subheader("🔤 Embeddings")
            embedder_provider = st.selectbox(
                "Provedor de Embeddings:",
                ["OpenAI", "HuggingFace", "Sentence Transformers"]
            )
            
            if embedder_provider == "OpenAI":
                embedding_model = st.selectbox(
                    "Modelo:",
                    ["text-embedding-3-small", "text-embedding-3-large", "text-embedding-ada-002"]
                )
                dimensions = st.slider("Dimensões:", 512, 3072, 1536)
            
            # Configurações RAG
            st.subheader("🔍 Configurações RAG")
            retrieval_method = st.selectbox(
                "Método de Recuperação:",
                ["Vetorial", "Híbrido", "Palavra-chave"]
            )
            
            top_k = st.slider("Top K Resultados:", 1, 20, 5)
            similarity_threshold = st.slider("Limiar de Similaridade:", 0.0, 1.0, 0.7)
        
        # Salvar configuração
        st.session_state.agent_configs['level_2'] = {
            "knowledge_type": knowledge_type,
            "knowledge_path": knowledge_path if knowledge_type in ["Documentos de Texto", "PDFs"] else None,
            "urls": urls_list if knowledge_type == "Websites" else None,
            "chunk_size": chunk_size,
            "chunk_overlap": chunk_overlap,
            "vector_db": vector_db,
            "embedder_provider": embedder_provider,
            "embedding_model": embedding_model if embedder_provider == "OpenAI" else None,
            "retrieval_method": retrieval_method,
            "top_k": top_k,
            "similarity_threshold": similarity_threshold
        }
        
        # Preview
        st.markdown("---")
        if st.button("🔄 Gerar Código RAG"):
            code = self.generate_level_2_code(st.session_state.agent_configs['level_2'])
            st.code(code, language="python")
    
    def render_level_3_builder(self):
        """Builder para Nível 3: Agentes com memória"""
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("🧠 Configurações de Memória")
            
            memory_types = st.multiselect(
                "Tipos de Memória:",
                ["Memória de Sessão", "Memória de Longo Prazo", "Memória Compartilhada", "Resumos de Sessão"],
                default=["Memória de Sessão"]
            )
            
            storage_type = st.selectbox(
                "Tipo de Armazenamento:",
                ["SQLite", "PostgreSQL", "MongoDB", "Redis", "Mem0", "Zep"]
            )
            
            if storage_type == "SQLite":
                db_file = st.text_input("Arquivo do Banco:", "memoria_agente.db")
            elif storage_type == "PostgreSQL":
                pg_url = st.text_input("URL PostgreSQL:", "postgresql://user:pass@localhost/db")
            
            # Configurações específicas de memória
            if "Memória de Longo Prazo" in memory_types:
                st.subheader("⏳ Memória de Longo Prazo")
                max_memories = st.slider("Máximo de Memórias:", 100, 10000, 1000)
                summarize_after = st.slider("Resumir após N mensagens:", 5, 50, 10)
                delete_old_memories = st.checkbox("Deletar memórias antigas")
            
            if "Memória Compartilhada" in memory_types:
                st.subheader("🤝 Memória Compartilhada")
                team_id = st.text_input("ID do Time:", "meu_time")
                shared_context = st.checkbox("Contexto compartilhado")
        
        with col2:
            st.subheader("🤔 Configurações de Raciocínio")
            
            reasoning_enabled = st.checkbox("Habilitar Raciocínio", value=True)
            
            if reasoning_enabled:
                reasoning_type = st.selectbox(
                    "Tipo de Raciocínio:",
                    ["ReasoningTools", "Chain-of-Thought", "Modelo de Raciocínio Nativo"]
                )
                
                show_reasoning = st.checkbox("Mostrar Processo de Raciocínio", value=True)
                stream_reasoning = st.checkbox("Stream do Raciocínio", value=True)
                
                if reasoning_type == "ReasoningTools":
                    add_reasoning_instructions = st.checkbox("Adicionar Instruções de Raciocínio", value=True)
                
                # Configurações avançadas de raciocínio
                with st.expander("🧠 Configurações Avançadas"):
                    reasoning_depth = st.slider("Profundidade do Raciocínio:", 1, 10, 3)
                    self_reflection = st.checkbox("Auto-reflexão")
                    multi_step_reasoning = st.checkbox("Raciocínio Multi-etapas")
            
            st.subheader("👤 Configurações de Usuário")
            user_id = st.text_input("ID do Usuário:", "usuario_padrao")
            enable_user_memories = st.checkbox("Habilitar Memórias do Usuário", value=True)
            personalization = st.checkbox("Personalização Baseada em Histórico")
        
        # Salvar configuração
        st.session_state.agent_configs['level_3'] = {
            "memory_types": memory_types,
            "storage_type": storage_type,
            "db_file": db_file if storage_type == "SQLite" else None,
            "reasoning_enabled": reasoning_enabled,
            "reasoning_type": reasoning_type if reasoning_enabled else None,
            "show_reasoning": show_reasoning if reasoning_enabled else False,
            "user_id": user_id,
            "enable_user_memories": enable_user_memories,
            "max_memories": max_memories if "Memória de Longo Prazo" in memory_types else None,
            "summarize_after": summarize_after if "Memória de Longo Prazo" in memory_types else None
        }
        
        # Preview
        st.markdown("---")
        if st.button("🔄 Gerar Código com Memória"):
            code = self.generate_level_3_code(st.session_state.agent_configs['level_3'])
            st.code(code, language="python")
    
    def render_level_4_builder(self):
        """Builder para Nível 4: Times de agentes"""
        st.subheader("👥 Configuração do Time")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            team_name = st.text_input("Nome do Time:", "Meu Time de Agentes")
            team_description = st.text_area(
                "Descrição do Time:",
                "Time especializado em resolver problemas complexos através da colaboração."
            )
            
            team_mode = st.selectbox(
                "Modo de Operação:",
                ["collaborate", "coordinate", "route"],
                help={
                    "collaborate": "Todos os agentes trabalham juntos na mesma tarefa",
                    "coordinate": "Agentes são coordenados automaticamente pelo sistema",
                    "route": "Tarefas são direcionadas para agentes específicos"
                }
            )
            
            # Configurações do time
            success_criteria = st.text_area(
                "Critérios de Sucesso:",
                "Resposta completa e bem estruturada com contribuições de todos os membros."
            )
            
            max_iterations = st.slider("Máximo de Iterações:", 1, 20, 5)
            show_member_responses = st.checkbox("Mostrar Respostas dos Membros", value=True)
        
        with col2:
            st.subheader("📊 Visualização do Time")
            
            # Mostrar diagrama do time baseado no modo
            if team_mode == "collaborate":
                st.info("🤝 Modo Colaborativo\nTodos os agentes trabalham juntos")
            elif team_mode == "coordinate":
                st.info("🎯 Modo Coordenado\nSistema coordena automaticamente")
            elif team_mode == "route":
                st.info("🔀 Modo Roteamento\nTarefas direcionadas por especialidade")
        
        # Configuração dos membros
        st.subheader("👨‍💼 Membros do Time")
        
        num_agents = st.slider("Número de Agentes:", 2, 10, 3)
        
        agents_config = []
        
        for i in range(num_agents):
            with st.expander(f"🤖 Agente {i+1}", expanded=i < 2):
                col_agent1, col_agent2 = st.columns(2)
                
                with col_agent1:
                    name = st.text_input(f"Nome:", f"Agente {i+1}", key=f"agent_name_{i}")
                    role = st.text_input(f"Função:", f"Especialista {i+1}", key=f"agent_role_{i}")
                    
                    specialization = st.selectbox(
                        f"Especialização:",
                        ["Pesquisa", "Análise", "Escrita", "Cálculos", "Criativo", "Técnico", "Financeiro"],
                        key=f"agent_spec_{i}"
                    )
                
                with col_agent2:
                    agent_model = st.selectbox(
                        f"Modelo:",
                        ["gpt-4", "gpt-3.5-turbo", "claude-3-sonnet"],
                        key=f"agent_model_{i}"
                    )
                    
                    # Ferramentas baseadas na especialização
                    if specialization == "Pesquisa":
                        default_tools = ["DuckDuckGo", "Google Search"]
                    elif specialization == "Análise":
                        default_tools = ["Calculator", "Pandas"]
                    elif specialization == "Financeiro":
                        default_tools = ["YFinance", "Calculator"]
                    else:
                        default_tools = ["Calculator"]
                    
                    agent_tools = st.multiselect(
                        f"Ferramentas:",
                        ["DuckDuckGo", "Calculator", "YFinance", "Pandas", "Email"],
                        default=default_tools,
                        key=f"agent_tools_{i}"
                    )
                
                agent_instructions = st.text_area(
                    f"Instruções Específicas:",
                    f"Você é um {specialization.lower()} especializado. Foque na sua área de expertise.",
                    key=f"agent_instructions_{i}",
                    height=80
                )
                
                agents_config.append({
                    "name": name,
                    "role": role,
                    "specialization": specialization,
                    "model": agent_model,
                    "tools": agent_tools,
                    "instructions": agent_instructions
                })
        
        # Salvar configuração
        st.session_state.agent_configs['level_4'] = {
            "team_name": team_name,
            "team_description": team_description,
            "team_mode": team_mode,
            "success_criteria": success_criteria,
            "max_iterations": max_iterations,
            "show_member_responses": show_member_responses,
            "agents": agents_config
        }
        
        # Preview
        st.markdown("---")
        if st.button("🔄 Gerar Código do Time"):
            code = self.generate_level_4_code(st.session_state.agent_configs['level_4'])
            st.code(code, language="python")
    
    def render_level_5_builder(self):
        """Builder para Nível 5: Workflows"""
        st.subheader("🔄 Configuração do Workflow")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            workflow_name = st.text_input("Nome do Workflow:", "Meu Workflow Agêntico")
            workflow_description = st.text_area(
                "Descrição:",
                "Workflow automatizado para processar tarefas complexas em etapas estruturadas."
            )
            
            workflow_type = st.selectbox(
                "Tipo de Workflow:",
                ["Sequencial", "Paralelo", "Condicional", "Loop", "Híbrido"]
            )
        
        with col2:
            st.subheader("⚙️ Configurações Gerais")
            
            max_retries = st.slider("Máximo de Tentativas:", 1, 10, 3)
            timeout_minutes = st.slider("Timeout (minutos):", 1, 60, 10)
            save_intermediate = st.checkbox("Salvar Estados Intermediários", value=True)
        
        # Configuração das etapas
        st.subheader("📋 Etapas do Workflow")
        
        num_steps = st.slider("Número de Etapas:", 2, 15, 4)
        
        steps_config = []
        
        for i in range(num_steps):
            with st.expander(f"📝 Etapa {i+1}", expanded=i < 2):
                col_step1, col_step2 = st.columns(2)
                
                with col_step1:
                    step_name = st.text_input(f"Nome da Etapa:", f"Etapa {i+1}", key=f"step_name_{i}")
                    step_description = st.text_area(
                        f"Descrição:",
                        f"Descrição da etapa {i+1}",
                        key=f"step_desc_{i}",
                        height=60
                    )
                    
                    step_type = st.selectbox(
                        f"Tipo:",
                        ["Agente", "Função", "Condição", "Loop", "Paralelo"],
                        key=f"step_type_{i}"
                    )
                
                with col_step2:
                    if step_type == "Agente":
                        agent_for_step = st.selectbox(
                            f"Agente:",
                            ["Pesquisador", "Analista", "Editor", "Especialista", "Novo Agente"],
                            key=f"step_agent_{i}"
                        )
                        
                        if agent_for_step == "Novo Agente":
                            custom_agent_name = st.text_input(f"Nome do Agente:", key=f"custom_agent_{i}")
                    
                    elif step_type == "Condição":
                        condition_type = st.selectbox(
                            f"Tipo de Condição:",
                            ["Resultado Anterior", "Valor Específico", "Função Personalizada"],
                            key=f"condition_type_{i}"
                        )
                    
                    # Dependências
                    available_steps = [f"Etapa {j+1}" for j in range(i)]
                    dependencies = st.multiselect(
                        f"Depende de:",
                        available_steps,
                        key=f"step_deps_{i}"
                    )
                
                # Configurações específicas da etapa
                if step_type == "Loop":
                    max_iterations = st.slider(f"Máx. Iterações:", 1, 20, 5, key=f"loop_max_{i}")
                    loop_condition = st.text_input(f"Condição de Parada:", key=f"loop_condition_{i}")
                
                steps_config.append({
                    "name": step_name,
                    "description": step_description,
                    "type": step_type,
                    "agent": agent_for_step if step_type == "Agente" else None,
                    "dependencies": dependencies,
                    "max_iterations": max_iterations if step_type == "Loop" else None
                })
        
        # Visualização do workflow
        st.subheader("🗺️ Visualização do Workflow")
        self.render_workflow_diagram(steps_config)
        
        # Salvar configuração
        st.session_state.agent_configs['level_5'] = {
            "workflow_name": workflow_name,
            "workflow_description": workflow_description,
            "workflow_type": workflow_type,
            "max_retries": max_retries,
            "timeout_minutes": timeout_minutes,
            "save_intermediate": save_intermediate,
            "steps": steps_config
        }
        
        # Preview
        st.markdown("---")
        if st.button("🔄 Gerar Código do Workflow"):
            code = self.generate_level_5_code(st.session_state.agent_configs['level_5'])
            st.code(code, language="python")
    
    def render_workflow_diagram(self, steps_config):
        """Renderiza diagrama do workflow usando Mermaid"""
        if not steps_config:
            st.info("Adicione etapas para visualizar o diagrama")
            return
        
        mermaid_code = "graph TD\n"
        
        for i, step in enumerate(steps_config):
            step_id = f"S{i+1}"
            step_label = step['name'].replace(' ', '_')
            
            # Definir formato baseado no tipo
            if step['type'] == "Agente":
                shape = f"{step_id}[{step_label}]"
            elif step['type'] == "Condição":
                shape = f"{step_id}{{{step_label}}}"
            elif step['type'] == "Loop":
                shape = f"{step_id}(({step_label}))"
            else:
                shape = f"{step_id}[{step_label}]"
            
            mermaid_code += f"    {shape}\n"
            
            # Adicionar dependências
            for dep in step.get('dependencies', []):
                try:
                    dep_index = next(j for j, s in enumerate(steps_config) if s['name'] == dep)
                    dep_id = f"S{dep_index + 1}"
                    mermaid_code += f"    {dep_id} --> {step_id}\n"
                except StopIteration:
                    continue
        
        st.code(mermaid_code, language="mermaid")
        
        # Tentar renderizar com streamlit se disponível
        try:
            st.markdown(f"```mermaid\n{mermaid_code}\n```")
        except:
            st.info("Para visualizar o diagrama, copie o código Mermaid acima para um visualizador online")
    
    def get_ai_suggestions(self, level: int):
        """Obtém sugestões da IA para o nível atual"""
        if not AGNO_AVAILABLE or not st.session_state.ai_assistant:
            st.warning("Assistente IA não disponível")
            return
        
        level_contexts = {
            1: "agente básico com ferramentas",
            2: "agente com base de conhecimento RAG",
            3: "agente com memória e raciocínio",
            4: "time de agentes colaborativos",
            5: "workflow agêntico complexo"
        }
        
        current_config = st.session_state.agent_configs.get(f'level_{level}', {})
        
        prompt = f"""
        Estou criando um {level_contexts[level]} no Agno Framework.
        
        Configuração atual: {json.dumps(current_config, indent=2)}
        
        Por favor, sugira:
        1. Melhorias na configuração atual
        2. Melhores práticas para este nível
        3. Ferramentas recomendadas
        4. Configurações otimizadas
        5. Exemplos de uso prático
        
        Seja específico e prático nas sugestões.
        """
        
        with st.spinner("🤖 Obtendo sugestões da IA..."):
            try:
                suggestion = st.session_state.ai_assistant.run(prompt)
                st.success("✅ Sugestões obtidas!")
                st.markdown("### 🤖 Sugestões da IA:")
                st.markdown(suggestion.content)
            except Exception as e:
                st.error(f"Erro ao obter sugestões: {e}")
    
    def load_template(self, level: int):
        """Carrega template pré-configurado para o nível"""
        templates = {
            1: {
                "name": "Assistente de Pesquisa",
                "role": "Pesquisador especializado",
                "model_provider": "OpenAI",
                "model_id": "gpt-4",
                "instructions": "Você é um pesquisador especializado.\nSempre cite suas fontes.\nUse múltiplas ferramentas para validar informações.",
                "tools": [
                    {"name": "DuckDuckGo", "class": "DuckDuckGoTools", "import": "agno.tools.duckduckgo"},
                    {"name": "Calculator", "class": "CalculatorTools", "import": "agno.tools.calculator"}
                ]
            },
            2: {
                "knowledge_type": "Documentos de Texto",
                "knowledge_path": "documentos/",
                "chunk_size": 1000,
                "chunk_overlap": 200,
                "vector_db": "ChromaDB",
                "embedder_provider": "OpenAI",
                "embedding_model": "text-embedding-3-small"
            },
            3: {
                "memory_types": ["Memória de Sessão", "Memória de Longo Prazo"],
                "storage_type": "SQLite",
                "db_file": "agente_memoria.db",
                "reasoning_enabled": True,
                "reasoning_type": "ReasoningTools"
            },
            4: {
                "team_name": "Time de Análise",
                "team_mode": "collaborate",
                "agents": [
                    {"name": "Pesquisador", "specialization": "Pesquisa", "tools": ["DuckDuckGo"]},
                    {"name": "Analista", "specialization": "Análise", "tools": ["Calculator", "Pandas"]},
                    {"name": "Editor", "specialization": "Escrita", "tools": []}
                ]
            },
            5: {
                "workflow_name": "Workflow de Análise",
                "workflow_type": "Sequencial",
                "steps": [
                    {"name": "Pesquisa", "type": "Agente", "agent": "Pesquisador"},
                    {"name": "Análise", "type": "Agente", "agent": "Analista"},
                    {"name": "Relatório", "type": "Agente", "agent": "Editor"}
                ]
            }
        }
        
        if level in templates:
            st.session_state.agent_configs[f'level_{level}'] = templates[level]
            st.success(f"✅ Template do Nível {level} carregado!")
            st.experimental_rerun()
    
    def save_configuration(self):
        """Salva configuração atual em arquivo"""
        config_data = {
            "timestamp": datetime.now().isoformat(),
            "current_level": st.session_state.current_level,
            "configurations": st.session_state.agent_configs
        }
        
        config_json = json.dumps(config_data, indent=2, ensure_ascii=False)
        
        st.download_button(
            label="💾 Download Configuração",
            data=config_json,
            file_name=f"agno_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
        
        st.success("✅ Configuração pronta para download!")
    
    def export_code(self):
        """Exporta código gerado"""
        if hasattr(st.session_state, 'generated_code') and st.session_state.generated_code:
            st.download_button(
                label="📤 Download Código Python",
                data=st.session_state.generated_code,
                file_name=f"agno_agent_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py",
                mime="text/plain"
            )
            st.success("✅ Código pronto para download!")
        else:
            st.warning("⚠️ Gere o código primeiro usando o botão 'Gerar Código'")
    
    def generate_level_1_code(self, config: Dict[str, Any]) -> str:
        """Gera código Python para agente Nível 1"""
        imports = ["from agno.agent import Agent"]
        
        # Import do modelo
        if config['model_provider'] == "OpenAI":
            imports.append("from agno.models.openai import OpenAIChat")
            model_class = "OpenAIChat"
        elif config['model_provider'] == "Anthropic":
            imports.append("from agno.models.anthropic import Claude")
            model_class = "Claude"
        elif config['model_provider'] == "Google Gemini":
            imports.append("from agno.models.google import Gemini")
            model_class = "Gemini"
        elif config['model_provider'] == "OpenRouter":
            imports.append("from agno.models.openrouter import OpenRouter")
            model_class = "OpenRouter"
        else:
            imports.append(f"from agno.models.{config['model_provider'].lower()} import {config['model_provider']}")
            model_class = config['model_provider']
        
        # Imports das ferramentas
        for tool in config['tools']:
            imports.append(f"from {tool['import']} import {tool['class']}")
        
        # Gerar código
        code = "\n".join(imports) + "\n\n"
        
        # Adicionar comentários sobre configuração de API
        if config['model_provider'] == "OpenRouter":
            code += """# Configuração OpenRouter
# Certifique-se de ter configurado: export OPENROUTER_API_KEY=sua_chave
# Obtenha sua chave em: https://openrouter.ai/keys

"""
        elif config['model_provider'] == "Google Gemini":
            code += """# Configuração Google Gemini
# Certifique-se de ter configurado: export GOOGLE_API_KEY=sua_chave
# Para Vertex AI: export GOOGLE_GENAI_USE_VERTEXAI=true

"""
        elif config['model_provider'] == "Anthropic":
            code += """# Configuração Anthropic
# Certifique-se de ter configurado: export ANTHROPIC_API_KEY=sua_chave

"""
        elif config['model_provider'] == "OpenAI":
            code += """# Configuração OpenAI
# Certifique-se de ter configurado: export OPENAI_API_KEY=sua_chave

"""
        
        # Criar nome da variável
        agent_var_name = config['name'].lower().replace(' ', '_')
        
        code += f"""# Criar {config['name']}
{agent_var_name} = Agent(
    name="{config['name']}",
    role="{config['role']}",
    model={model_class}(id="{config['model_id']}"),"""
        
        if config['tools']:
            code += "\n    tools=[\n"
            for tool in config['tools']:
                if tool['name'] == "YFinance":
                    code += f"        {tool['class']}(stock_price=True, analyst_recommendations=True),\n"
                else:
                    code += f"        {tool['class']}(),\n"
            code += "    ],"
        
        instructions_formatted = config['instructions'].replace('\n', '",\n        "')
        
        code += f"""
    instructions=[
        "{instructions_formatted}"
    ],
    show_tool_calls={config['show_tool_calls']},
    markdown={config['markdown']},
)

# Testar o agente
{agent_var_name}.print_response(
    "Olá! Como você pode me ajudar?",
    stream={config['stream']}
)
"""
        
        return code
    
    def generate_level_2_code(self, config: Dict[str, Any]) -> str:
        """Gera código Python para agente Nível 2 (RAG)"""
        code = """from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude
from agno.models.google import Gemini
from agno.models.openrouter import OpenRouter
from agno.knowledge.text import TextKnowledgeBase
from agno.vectordb.chroma import ChromaDb

# Configurar base de conhecimento
"""
        
        if config['knowledge_type'] == "Documentos de Texto":
            code += f"""knowledge_base = TextKnowledgeBase(
    path="{config['knowledge_path']}",
    vector_db=ChromaDb(
        collection="minha_base",
        path="vectordb/"
    ),
    chunk_size={config['chunk_size']},
    chunk_overlap={config['chunk_overlap']}
)"""
        
        code += f"""

# Criar agente com conhecimento
# Escolha o modelo desejado descomentando uma das linhas abaixo:
# model = OpenAIChat(id="gpt-4")  # OpenAI
# model = Claude(id="claude-3-5-sonnet")  # Anthropic
# model = Gemini(id="gemini-2.0-flash-001")  # Google
# model = OpenRouter(id="openai/gpt-4o")  # OpenRouter

agente_rag = Agent(
    model=OpenAIChat(id="gpt-4"),  # Altere conforme necessário
    knowledge=knowledge_base,
    instructions=[
        "Use a base de conhecimento para responder perguntas.",
        "Sempre cite as fontes das informações.",
        "Se não encontrar informação relevante, diga claramente."
    ],
    markdown=True,
)

# Carregar base de conhecimento (executar apenas uma vez)
agente_rag.knowledge.load(recreate=False)

# Testar o agente
agente_rag.print_response("Faça uma pergunta sobre o conteúdo da base de conhecimento")
"""
        
        return code
    
    def generate_level_3_code(self, config: Dict[str, Any]) -> str:
        """Gera código Python para agente Nível 3 (Memória)"""
        code = """from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.memory.v2 import Memory
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.storage.sqlite import SqliteStorage
"""
        
        if config['reasoning_enabled']:
            code += "from agno.tools.reasoning import ReasoningTools\n"
        
        code += f"""
# Configurar memória
memory = Memory(
    model=OpenAIChat(id="gpt-4"),
    db=SqliteMemoryDb(
        table_name="memorias_usuario",
        db_file="{config.get('db_file', 'memoria.db')}"
    )
)

# Configurar armazenamento
storage = SqliteStorage(
    table_name="sessoes_agente",
    db_file="{config.get('db_file', 'memoria.db')}"
)

# Criar agente com memória
agente_memoria = Agent(
    model=OpenAIChat(id="gpt-4"),
    memory=memory,
    storage=storage,
    user_id="{config['user_id']}",
    enable_user_memories={config['enable_user_memories']},
"""
        
        if config['reasoning_enabled']:
            code += """    tools=[ReasoningTools(add_instructions=True)],"""
        
        code += f"""
    instructions=[
        "Você é um assistente com memória.",
        "Lembre-se das conversas anteriores.",
        "Use o contexto histórico para personalizar respostas.",
        "Mantenha um relacionamento consistente com o usuário."
    ],
    add_history_to_messages=True,
    markdown=True,
)

# Testar o agente
agente_memoria.print_response(
    "Olá! Me conte algo sobre você para que eu possa lembrar.",
    {"show_full_reasoning" if config['reasoning_enabled'] else "stream"}: True
)
"""
        
        return code
    
    def generate_level_4_code(self, config: Dict[str, Any]) -> str:
        """Gera código Python para Time de Agentes (Nível 4)"""
        code = """from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools
from agno.tools.yfinance import YFinanceTools

"""
        
        # Gerar código para cada agente
        for i, agent_config in enumerate(config['agents']):
            tools_code = ""
            if agent_config['tools']:
                tools_map = {
                    "DuckDuckGo": "DuckDuckGoTools()",
                    "Calculator": "CalculatorTools()",
                    "YFinance": "YFinanceTools(stock_price=True)",
                    "Pandas": "PandasTools()",
                    "Email": "EmailTools()"
                }
                
                tools_list = [tools_map.get(tool, f"{tool}Tools()") for tool in agent_config['tools']]
                tools_code = f"    tools=[{', '.join(tools_list)}],"
            
            agent_var_name = agent_config['name'].lower().replace(' ', '_')
            
            code += f"""# {agent_config['name']}
{agent_var_name} = Agent(
    name="{agent_config['name']}",
    role="{agent_config['role']}",
    model=OpenAIChat(id="{agent_config['model']}"),
{tools_code}
    instructions=[
        "{agent_config['instructions']}"
    ],
    show_tool_calls=True,
    markdown=True,
)

"""
        
        # Gerar código do time
        agent_names = [agent['name'].lower().replace(' ', '_') for agent in config['agents']]
        team_var_name = config['team_name'].lower().replace(' ', '_')
        
        code += f"""# Criar time
{team_var_name} = Team(
    name="{config['team_name']}",
    members=[{', '.join(agent_names)}],
    model=OpenAIChat(id="gpt-4"),
    mode="{config['team_mode']}",
    success_criteria="{config['success_criteria']}",
    instructions=[
        "Trabalhem juntos para fornecer respostas completas.",
        "Cada agente deve contribuir com sua especialidade.",
        "Mantenham comunicação clara entre os membros."
    ],
    show_tool_calls=True,
    show_members_responses={config['show_member_responses']},
    markdown=True,
)

# Testar o time
{team_var_name}.print_response(
    "Trabalhem juntos para resolver este problema complexo: "
    "Analisem o mercado de tecnologia e criem um relatório completo.",
    stream=True
)
"""
        
        return code
    
    def generate_level_5_code(self, config: Dict[str, Any]) -> str:
        """Gera código Python para Workflow (Nível 5)"""
        code = """from agno.agent import Agent
from agno.workflow import Workflow
from agno.workflow.task import Task
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.calculator import CalculatorTools

# Criar agentes para o workflow
pesquisador = Agent(
    name="Pesquisador",
    model=OpenAIChat(id="gpt-4"),
    tools=[DuckDuckGoTools()],
    instructions=["Pesquise informações detalhadas sobre o tópico."]
)

analista = Agent(
    name="Analista", 
    model=OpenAIChat(id="gpt-4"),
    tools=[CalculatorTools()],
    instructions=["Analise os dados coletados e faça cálculos necessários."]
)

editor = Agent(
    name="Editor",
    model=OpenAIChat(id="gpt-4"),
    instructions=["Compile as informações em um relatório final bem estruturado."]
)

"""
        
        # Gerar tarefas
        for i, step in enumerate(config['steps']):
            agent_map = {
                "Pesquisador": "pesquisador",
                "Analista": "analista", 
                "Editor": "editor"
            }
            
            agent_var = agent_map.get(step.get('agent', 'pesquisador'), 'pesquisador')
            deps = f"depends_on={step['dependencies']}" if step['dependencies'] else ""
            
            code += f"""# Tarefa: {step['name']}
tarefa_{i+1} = Task(
    name="{step['name'].lower().replace(' ', '_')}",
    agent={agent_var},
    description="{step['description']}",
    {deps}
)

"""
        
        # Gerar workflow
        task_names = [f"tarefa_{i+1}" for i in range(len(config['steps']))]
        workflow_var_name = config['workflow_name'].lower().replace(' ', '_')
        
        code += f"""# Criar workflow
{workflow_var_name} = Workflow(
    name="{config['workflow_name']}",
    description="{config['workflow_description']}",
    tasks=[{', '.join(task_names)}],
    max_retries={config['max_retries']},
)

# Executar workflow
resultado = {workflow_var_name}.run(
    input_data={{"topico": "Análise de mercado de IA"}}
)

print("Resultado do Workflow:")
print(resultado.content)
"""
        
        return code
    
    def initialize_streamlit(self):
        """Inicializa configurações do Streamlit"""
        try:
            # Configurar página do Streamlit
            st.set_page_config(
                page_title="Agno Agent Builder",
                page_icon="🤖",
                layout="wide",
                initial_sidebar_state="expanded"
            )
        except:
            # Página já foi configurada
            pass
        
        # Inicializar estado da sessão
        if 'current_level' not in st.session_state:
            st.session_state.current_level = 1
        if 'agent_configs' not in st.session_state:
            st.session_state.agent_configs = {}
        if 'ai_assistant' not in st.session_state and AGNO_AVAILABLE:
            st.session_state.ai_assistant = self.create_ai_assistant()
        if 'openrouter_models' not in st.session_state:
            st.session_state.openrouter_models = self.get_openrouter_models()
        if 'app_logs' not in st.session_state:
            st.session_state.app_logs = []
    
    def add_log(self, message: str, level: str = "INFO"):
        """Adiciona uma mensagem ao log da aplicação"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {level}: {message}"
        st.session_state.app_logs.append(log_entry)
        
        # Manter apenas os últimos 100 logs
        if len(st.session_state.app_logs) > 100:
            st.session_state.app_logs = st.session_state.app_logs[-100:]
    
    def test_api_connection(self, provider: str, api_key: str) -> bool:
        """Testa conexão com API do provedor"""
        try:
            if provider == "OpenAI/OpenRouter":
                import requests
                headers = {"Authorization": f"Bearer {api_key}"}
                if api_key.startswith("sk-or-"):
                    # OpenRouter
                    response = requests.get("https://openrouter.ai/api/v1/models", 
                                          headers=headers, timeout=5)
                else:
                    # OpenAI
                    response = requests.get("https://api.openai.com/v1/models", 
                                          headers=headers, timeout=5)
                return response.status_code == 200
            
            elif provider == "Anthropic":
                import requests
                headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01"}
                response = requests.get("https://api.anthropic.com/v1/messages", 
                                      headers=headers, timeout=5)
                return response.status_code in [200, 400]  # 400 é esperado sem body
            
            elif provider == "Google":
                import requests
                response = requests.get(f"https://generativelanguage.googleapis.com/v1/models?key={api_key}", 
                                      timeout=5)
                return response.status_code == 200
            
            return False
        except Exception as e:
            self.add_log(f"Erro ao testar {provider}: {e}", "ERROR")
            return False
    
    def render_settings_tab(self):
        """Renderiza a aba de configurações"""
        st.header("⚙️ Configurações")
        
        # Sub-abas dentro de Settings
        settings_tab1, settings_tab2, settings_tab3 = st.tabs(["🔑 APIs", "📊 Logs", "🔧 Sistema"])
        
        with settings_tab1:
            self.render_api_settings()
        
        with settings_tab2:
            self.render_logs_section()
        
        with settings_tab3:
            self.render_system_settings()
    
    def render_api_settings(self):
        """Renderiza configurações de APIs"""
        st.subheader("🔑 Configuração de APIs")
        
        # Carregar configurações atuais do .env
        current_apis = {
            "OpenAI/OpenRouter": os.getenv("OPENAI_API_KEY", ""),
            "Anthropic": os.getenv("ANTHROPIC_API_KEY", ""),
            "Google": os.getenv("GOOGLE_API_KEY", "")
        }
        
        # Interface para cada API
        for provider, current_key in current_apis.items():
            with st.expander(f"🔧 {provider}", expanded=bool(current_key)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Campo para inserir chave
                    key_input = st.text_input(
                        f"Chave da API {provider}:",
                        value=current_key,
                        type="password",
                        key=f"api_key_{provider}",
                        help=self.get_api_help(provider)
                    )
                
                with col2:
                    # Botão de teste
                    if st.button(f"🧪 Testar", key=f"test_{provider}"):
                        if key_input:
                            with st.spinner(f"Testando {provider}..."):
                                if self.test_api_connection(provider, key_input):
                                    st.success(f"✅ {provider} funcionando!")
                                    self.add_log(f"Teste de API {provider}: SUCESSO")
                                else:
                                    st.error(f"❌ {provider} falhou!")
                                    self.add_log(f"Teste de API {provider}: FALHOU", "ERROR")
                        else:
                            st.warning("⚠️ Insira uma chave primeiro")
                
                # Salvar configuração
                if key_input != current_key:
                    if st.button(f"💾 Salvar {provider}", key=f"save_{provider}"):
                        self.save_api_key(provider, key_input)
                        st.success(f"✅ Chave do {provider} salva!")
                        self.add_log(f"Chave API {provider} atualizada")
                        st.rerun()
                
                # Status atual
                if current_key:
                    masked_key = current_key[:8] + "..." + current_key[-4:] if len(current_key) > 12 else "***"
                    st.info(f"🔑 Chave atual: {masked_key}")
                else:
                    st.warning("⚠️ Nenhuma chave configurada")
        
        # Instruções
        st.markdown("---")
        st.markdown("""
        ### 📋 Como obter chaves de API:
        
        **🔵 OpenAI:**
        - Acesse: https://platform.openai.com/api-keys
        - Crie uma conta e gere uma chave
        - Formato: `sk-proj-...`
        
        **🌐 OpenRouter:**
        - Acesse: https://openrouter.ai/keys
        - Crie uma conta gratuita
        - Formato: `sk-or-v1-...`
        - 💡 Tem modelos gratuitos disponíveis!
        
        **🟠 Anthropic:**
        - Acesse: https://console.anthropic.com/
        - Crie uma conta e gere uma chave
        - Formato: `sk-ant-api03-...`
        
        **🔴 Google Gemini:**
        - Acesse: https://makersuite.google.com/app/apikey
        - Faça login com conta Google
        - Formato: `AIzaSy...`
        - 💡 Tem cota gratuita generosa!
        """)
    
    def get_api_help(self, provider: str) -> str:
        """Retorna texto de ajuda para cada provedor"""
        help_texts = {
            "OpenAI/OpenRouter": "Para OpenAI use sk-proj-... Para OpenRouter use sk-or-v1-...",
            "Anthropic": "Chave da Anthropic no formato sk-ant-api03-...",
            "Google": "Chave do Google AI no formato AIzaSy..."
        }
        return help_texts.get(provider, "")
    
    def save_api_key(self, provider: str, api_key: str):
        """Salva chave de API no arquivo .env"""
        env_vars = {
            "OpenAI/OpenRouter": "OPENAI_API_KEY",
            "Anthropic": "ANTHROPIC_API_KEY", 
            "Google": "GOOGLE_API_KEY"
        }
        
        env_var = env_vars.get(provider)
        if env_var:
            # Atualizar variável de ambiente atual
            os.environ[env_var] = api_key
            
            # Atualizar arquivo .env
            self.update_env_file(env_var, api_key)
    
    def update_env_file(self, key: str, value: str):
        """Atualiza arquivo .env com nova chave"""
        env_file = ".env"
        lines = []
        key_found = False
        
        # Ler arquivo existente
        if os.path.exists(env_file):
            with open(env_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        
        # Atualizar ou adicionar chave
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                key_found = True
                break
        
        if not key_found:
            lines.append(f"{key}={value}\n")
        
        # Escrever arquivo
        with open(env_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
    
    def render_logs_section(self):
        """Renderiza seção de logs"""
        st.subheader("📊 Logs da Aplicação")
        
        col1, col2, col3 = st.columns([1, 1, 2])
        
        with col1:
            if st.button("🔄 Atualizar Logs"):
                st.rerun()
        
        with col2:
            if st.button("🗑️ Limpar Logs"):
                st.session_state.app_logs = []
                st.success("✅ Logs limpos!")
                st.rerun()
        
        with col3:
            log_level = st.selectbox("Filtrar por nível:", ["TODOS", "INFO", "ERROR", "WARNING"])
        
        # Mostrar logs
        if st.session_state.app_logs:
            # Filtrar logs se necessário
            filtered_logs = st.session_state.app_logs
            if log_level != "TODOS":
                filtered_logs = [log for log in st.session_state.app_logs if log_level in log]
            
            # Mostrar logs em ordem reversa (mais recentes primeiro)
            st.text_area(
                "📋 Logs:",
                value="\n".join(reversed(filtered_logs)),
                height=400,
                disabled=True
            )
            
            st.info(f"📊 Total de logs: {len(st.session_state.app_logs)} | Filtrados: {len(filtered_logs)}")
        else:
            st.info("📝 Nenhum log disponível ainda")
        
        # Adicionar log de teste
        if st.button("🧪 Adicionar Log de Teste"):
            self.add_log("Este é um log de teste", "INFO")
            st.success("✅ Log de teste adicionado!")
            st.rerun()
    
    def render_system_settings(self):
        """Renderiza configurações do sistema"""
        st.subheader("🔧 Configurações do Sistema")
        
        # Informações do sistema
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🐍 Ambiente Python:**")
            st.info(f"Versão: {sys.version}")
            st.info(f"Executável: {sys.executable}")
            
            # Verificar ambiente virtual
            if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
                st.success("✅ Ambiente virtual ativo")
            else:
                st.warning("⚠️ Ambiente virtual não detectado")
        
        with col2:
            st.markdown("**📦 Dependências:**")
            
            # Verificar dependências principais
            deps = {
                "streamlit": "Interface web",
                "agno": "Framework principal", 
                "openai": "Cliente OpenAI",
                "anthropic": "Cliente Anthropic",
                "google-generativeai": "Cliente Google"
            }
            
            for dep, desc in deps.items():
                try:
                    __import__(dep.replace('-', '_'))
                    st.success(f"✅ {dep}")
                except ImportError:
                    st.error(f"❌ {dep}")
        
        # Configurações avançadas
        st.markdown("---")
        st.markdown("**⚙️ Configurações Avançadas:**")
        
        # Protobuf
        current_protobuf = os.getenv("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", "")
        protobuf_setting = st.selectbox(
            "Implementação Protobuf:",
            ["python", "cpp", "upb"],
            index=0 if current_protobuf == "python" else 1
        )
        
        if protobuf_setting != current_protobuf:
            if st.button("💾 Salvar Configuração Protobuf"):
                os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = protobuf_setting
                self.update_env_file("PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION", protobuf_setting)
                st.success("✅ Configuração salva! Reinicie a aplicação.")
                self.add_log(f"Protobuf configurado para: {protobuf_setting}")
        
        # Cache
        if st.button("🗑️ Limpar Cache"):
            # Limpar cache do Streamlit
            st.cache_data.clear()
            if hasattr(st, 'cache_resource'):
                st.cache_resource.clear()
            
            # Limpar cache do OpenRouter
            try:
                from openrouter_api import ModelCache
                cache = ModelCache()
                cache.clear_cache()
            except:
                pass
            
            st.success("✅ Cache limpo!")
            self.add_log("Cache da aplicação limpo")
        
        # Reiniciar aplicação
        if st.button("🔄 Reiniciar Aplicação"):
            st.success("✅ Reiniciando...")
            self.add_log("Aplicação reiniciada pelo usuário")
            st.rerun()
    
    def run(self):
        """Executa a aplicação principal"""
        # Inicializar Streamlit
        self.initialize_streamlit()
        
        # Renderizar barra lateral
        current_level = self.render_sidebar()
        
        # Renderizar cabeçalho
        self.render_header(current_level)
        
        # Criar abas principais
        tab1, tab2 = st.tabs(["🤖 Agent Builder", "⚙️ Settings"])
        
        with tab1:
            # Renderizar builder baseado no nível
            if current_level == 1:
                self.render_level_1_builder()
            elif current_level == 2:
                self.render_level_2_builder()
            elif current_level == 3:
                self.render_level_3_builder()
            elif current_level == 4:
                self.render_level_4_builder()
            elif current_level == 5:
                self.render_level_5_builder()
            
            # Rodapé
            st.markdown("---")
            st.markdown("""
            ### 🚀 Próximos Passos
            1. **Configure** seu agente usando os controles acima
            2. **Gere o código** clicando no botão correspondente
            3. **Teste** o código em seu ambiente local
            4. **Monitore** o desempenho em https://app.agno.com
            
            ### 📚 Recursos Úteis
            - [Documentação Oficial](https://docs.agno.com)
            - [Exemplos no GitHub](https://github.com/agno-agi/agno/tree/main/cookbook)
            - [Comunidade Discord](https://discord.gg/4MtYHHrgA8)
            """)
        
        with tab2:
            self.render_settings_tab()

def main():
    """Função principal da aplicação"""
    builder = AgnoAgentBuilder()
    builder.run()

if __name__ == "__main__":
    main()