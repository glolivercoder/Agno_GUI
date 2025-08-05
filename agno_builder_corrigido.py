#!/usr/bin/env python3
"""
Agno Agent Builder - Versão Corrigida
Interface gráfica corrigida para criação de agentes Agno
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# Carregar e gerenciar variáveis de ambiente do arquivo .env
def load_env_file():
    """Carrega variáveis do arquivo .env se existir"""
    env_path = Path(".env")
    env_vars = {}
    
    if env_path.exists():
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        env_vars[key] = value
                        if value and not value.startswith('xxx'):
                            os.environ[key] = value
            return env_vars
        except Exception:
            pass
    return env_vars

def save_env_file(env_vars):
    """Salva variáveis no arquivo .env"""
    env_path = Path(".env")
    
    # Template do arquivo .env
    template = """# Agno Agent Builder - Configuração de APIs
# Configure suas chaves de API aqui

# PARA USAR OPENROUTER: Coloque sua chave do OpenRouter aqui
# Obtenha em: https://openrouter.ai/keys
OPENAI_API_KEY={openai_key}

# OU para usar OpenRouter específico:
OPENROUTER_API_KEY={openrouter_key}

# Anthropic - https://console.anthropic.com/
ANTHROPIC_API_KEY={anthropic_key}

# Google Gemini - https://makersuite.google.com/app/apikey
GOOGLE_API_KEY={google_key}

# Configurações adicionais
OPENROUTER_HTTP_REFERER=http://localhost:8501
OPENROUTER_X_TITLE=Agno Builder

# Configuração do protobuf para compatibilidade
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
"""
    
    try:
        content = template.format(
            openai_key=env_vars.get('OPENAI_API_KEY', ''),
            openrouter_key=env_vars.get('OPENROUTER_API_KEY', ''),
            anthropic_key=env_vars.get('ANTHROPIC_API_KEY', ''),
            google_key=env_vars.get('GOOGLE_API_KEY', '')
        )
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Atualizar variáveis de ambiente
        for key, value in env_vars.items():
            if value:
                os.environ[key] = value
        
        return True
    except Exception as e:
        print(f"Erro ao salvar .env: {e}")
        return False

def get_env_vars():
    """Obtém variáveis de ambiente atuais"""
    return {
        'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY', ''),
        'OPENROUTER_API_KEY': os.getenv('OPENROUTER_API_KEY', ''),
        'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY', ''),
        'GOOGLE_API_KEY': os.getenv('GOOGLE_API_KEY', '')
    }

# Carregar .env no início
env_data = load_env_file()

# Configurar protobuf
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

# Configurar página
st.set_page_config(
    page_title="🤖 Agno Agent Builder",
    page_icon="🤖",
    layout="wide"
)

def create_ai_assistant():
    """Cria assistente IA baseado nas chaves disponíveis"""
    try:
        import agno
        from agno.agent import Agent
        
        # Verificar chaves disponíveis
        env_vars = get_env_vars()
        
        # Tentar OpenRouter primeiro (modelos gratuitos)
        if env_vars.get('OPENAI_API_KEY') and env_vars['OPENAI_API_KEY'].startswith('sk-or-v1-'):
            from agno.models.openrouter import OpenRouter
            return Agent(
                name="Assistente IA (OpenRouter)",
                model=OpenRouter(id="mistralai/mistral-7b-instruct:free"),
                instructions=["Você é um assistente especializado em Agno Framework.", "Seja útil e preciso."],
                markdown=True
            )
        
        # Tentar Google Gemini
        elif env_vars.get('GOOGLE_API_KEY'):
            from agno.models.google import Gemini
            return Agent(
                name="Assistente IA (Gemini)",
                model=Gemini(id="gemini-2.0-flash-001"),
                instructions=["Você é um assistente especializado em Agno Framework.", "Seja útil e preciso."],
                markdown=True
            )
        
        # Tentar Anthropic
        elif env_vars.get('ANTHROPIC_API_KEY'):
            from agno.models.anthropic import Claude
            return Agent(
                name="Assistente IA (Claude)",
                model=Claude(id="claude-3-haiku"),
                instructions=["Você é um assistente especializado em Agno Framework.", "Seja útil e preciso."],
                markdown=True
            )
        
        # Tentar OpenAI
        elif env_vars.get('OPENAI_API_KEY'):
            from agno.models.openai import OpenAIChat
            return Agent(
                name="Assistente IA (OpenAI)",
                model=OpenAIChat(id="gpt-3.5-turbo"),
                instructions=["Você é um assistente especializado em Agno Framework.", "Seja útil e preciso."],
                markdown=True
            )
        
        return None
        
    except Exception as e:
        print(f"Erro ao criar assistente IA: {e}")
        return None

def main():
    """Interface principal corrigida"""
    
    # Título
    st.title("🤖 Agno Agent Builder - Versão Corrigida")
    st.markdown("### Interface Visual para Criação de Agentes Agno")
    
    # Verificar Agno
    try:
        import agno
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        from agno.models.anthropic import Claude
        from agno.models.google import Gemini
        from agno.models.openrouter import OpenRouter
        st.success("✅ Agno Framework carregado com sucesso!")
    except ImportError as e:
        st.error(f"""
        ❌ **Agno não está instalado**
        
        **Instale com:** `pip install agno`
        
        **Erro:** {e}
        """)
        return
    
    # Verificar e mostrar status das APIs
    env_vars = get_env_vars()
    configured_apis = [k.replace('_API_KEY', '') for k, v in env_vars.items() if v]
    
    if configured_apis:
        st.success(f"🔑 APIs configuradas: {', '.join(configured_apis)}")
        
        # Tentar criar assistente IA
        if 'ai_assistant' not in st.session_state:
            st.session_state.ai_assistant = create_ai_assistant()
            if st.session_state.ai_assistant:
                st.info(f"🤖 Assistente IA ativo: {st.session_state.ai_assistant.name}")
    else:
        st.warning("⚠️ Nenhuma API configurada. Configure na aba Settings.")
    
    # Inicializar session state
    if 'current_level' not in st.session_state:
        st.session_state.current_level = 1
    if 'agent_configs' not in st.session_state:
        st.session_state.agent_configs = {}
    if 'templates_loaded' not in st.session_state:
        st.session_state.templates_loaded = False
    
    # Abas principais
    tab1, tab2, tab3 = st.tabs(["🛠️ Builder", "📋 Templates", "⚙️ Settings"])
    
    with tab1:
        render_builder_tab()
    
    with tab2:
        render_templates_tab()
    
    with tab3:
        render_settings_tab()

def render_builder_tab():
    """Renderiza a aba do builder"""
    
    # Barra lateral
    st.sidebar.title("🎯 Configurações")
    
    # Seleção de nível
    nivel = st.sidebar.selectbox(
        "Nível do Agente:",
        [1, 2, 3, 4, 5],
        format_func=lambda x: f"Nível {x}: {get_level_name(x)}"
    )
    
    st.session_state.current_level = nivel
    
    st.sidebar.markdown(f"**Sobre Nível {nivel}:**")
    st.sidebar.info(get_level_description(nivel))
    
    # Status das APIs
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🔑 Status das APIs")
    render_api_status_sidebar()
    
    # Área principal
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"🛠️ Configurar Agente - Nível {nivel}")
        
        # Configurações básicas
        nome = st.text_input("Nome do Agente:", "Meu Agente")
        papel = st.text_input("Papel/Função:", "Assistente especializado")
        
        # Modelo
        provedor = st.selectbox(
            "Provedor do Modelo:",
            ["OpenAI", "Anthropic", "Google Gemini", "OpenRouter"]
        )
        
        modelo = get_model_options(provedor)
        modelo_selecionado = st.selectbox("Modelo:", modelo)
        
        # Instruções
        instrucoes = st.text_area(
            "Instruções:",
            "Você é um assistente útil e especializado.\nSempre seja claro e preciso.",
            height=100
        )
        
        # Ferramentas (apenas para níveis que suportam)
        ferramentas = []
        if nivel >= 1:
            st.subheader("🔧 Ferramentas")
            
            ferramentas_disponiveis = {
                "DuckDuckGo": st.checkbox("🔍 Busca DuckDuckGo"),
                "Calculator": st.checkbox("🧮 Calculadora"),
                "YFinance": st.checkbox("💰 Dados Financeiros"),
                "Email": st.checkbox("📧 Email"),
                "Python": st.checkbox("🐍 Python")
            }
            
            ferramentas = [nome for nome, selecionado in ferramentas_disponiveis.items() if selecionado]
    
    with col2:
        st.subheader("📋 Resumo")
        
        config = {
            "nome": nome,
            "papel": papel,
            "provedor": provedor,
            "modelo": modelo_selecionado,
            "instrucoes": instrucoes,
            "ferramentas": ferramentas,
            "nivel": nivel
        }
        
        # Salvar no session state
        st.session_state.agent_configs[f'level_{nivel}'] = config
        
        st.json(config)
        
        # Botões de ação
        if st.button("🔄 Gerar Código", type="primary"):
            codigo = gerar_codigo(config)
            st.subheader("📝 Código Gerado")
            st.code(codigo, language="python")
            
            # Download
            st.download_button(
                "📥 Download Código",
                codigo,
                f"agente_{nome.lower().replace(' ', '_')}.py",
                "text/plain"
            )
        
        if st.button("💾 Salvar Configuração"):
            config_json = json.dumps(config, indent=2, ensure_ascii=False)
            st.download_button(
                "📥 Download Config",
                config_json,
                f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                "application/json"
            )

def render_templates_tab():
    """Renderiza a aba de templates"""
    st.header("📋 Templates Pré-configurados")
    st.markdown("Carregue configurações prontas para diferentes tipos de agentes.")
    
    # Templates disponíveis
    templates = get_templates()
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🎯 Selecionar Template")
        
        template_names = list(templates.keys())
        selected_template = st.selectbox(
            "Escolha um template:",
            template_names,
            help="Selecione um template para carregar configurações pré-definidas"
        )
        
        if st.button("📋 Carregar Template", type="primary"):
            if selected_template in templates:
                template_data = templates[selected_template]
                nivel = template_data.get("nivel", 1)
                
                # Carregar no session state
                st.session_state.agent_configs[f'level_{nivel}'] = template_data
                st.session_state.current_level = nivel
                st.session_state.templates_loaded = True
                
                st.success(f"✅ Template '{selected_template}' carregado!")
                st.info(f"🤖 Usando provedor: {template_data.get('provedor', 'N/A')} - Modelo: {template_data.get('modelo', 'N/A')}")
                st.info(f"🎯 Vá para a aba Builder para ver as configurações do Nível {nivel}")
                st.rerun()
    
    with col2:
        st.subheader("📖 Detalhes do Template")
        
        if selected_template in templates:
            template_data = templates[selected_template]
            
            st.markdown(f"**Nome:** {template_data.get('nome', 'N/A')}")
            st.markdown(f"**Nível:** {template_data.get('nivel', 'N/A')}")
            st.markdown(f"**Provedor:** {template_data.get('provedor', 'N/A')}")
            st.markdown(f"**Modelo:** {template_data.get('modelo', 'N/A')}")
            
            if template_data.get('ferramentas'):
                st.markdown("**Ferramentas:**")
                for ferramenta in template_data['ferramentas']:
                    st.markdown(f"- {ferramenta}")
            
            if template_data.get('instrucoes'):
                st.markdown("**Instruções:**")
                st.code(template_data['instrucoes'])

def get_templates():
    """Retorna templates pré-configurados com detecção automática de provedor"""
    import os
    
    # Detectar provedor preferido baseado nas chaves de API disponíveis
    preferred_provider = "OpenRouter"
    preferred_model = "mistralai/mistral-7b-instruct:free"
    
    if os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY"):
        preferred_provider = "OpenRouter"
        preferred_model = "mistralai/mistral-7b-instruct:free"
    elif os.getenv("GOOGLE_API_KEY"):
        preferred_provider = "Google Gemini"
        preferred_model = "gemini-2.0-flash-001"
    elif os.getenv("ANTHROPIC_API_KEY"):
        preferred_provider = "Anthropic"
        preferred_model = "claude-3-haiku"
    elif os.getenv("OPENAI_API_KEY"):
        preferred_provider = "OpenAI"
        preferred_model = "gpt-3.5-turbo"
    
    return {
        "🔍 Assistente de Pesquisa": {
            "nome": "Assistente de Pesquisa",
            "papel": "Pesquisador especializado",
            "provedor": preferred_provider,
            "modelo": preferred_model,
            "instrucoes": "Você é um pesquisador especializado.\nSempre cite suas fontes.\nUse múltiplas ferramentas para validar informações.\nSeja preciso e objetivo.",
            "ferramentas": ["DuckDuckGo", "Calculator"],
            "nivel": 1
        },
        "💰 Analista Financeiro": {
            "nome": "Analista Financeiro",
            "papel": "Especialista em análise financeira",
            "provedor": preferred_provider,
            "modelo": preferred_model,
            "instrucoes": "Você é um analista financeiro experiente.\nUse dados atuais do mercado.\nForneça análises detalhadas e recomendações.\nSempre inclua disclaimers sobre riscos.",
            "ferramentas": ["YFinance", "Calculator", "DuckDuckGo"],
            "nivel": 1
        },
        "🐍 Assistente de Programação": {
            "nome": "Assistente de Programação",
            "papel": "Desenvolvedor especializado",
            "provedor": preferred_provider,
            "modelo": preferred_model,
            "instrucoes": "Você é um desenvolvedor experiente.\nEscreva código limpo e bem documentado.\nExplique suas soluções passo a passo.\nSiga as melhores práticas de programação.",
            "ferramentas": ["Calculator", "DuckDuckGo"],
            "nivel": 1
        },
        "📚 Assistente Educacional": {
            "nome": "Assistente Educacional",
            "papel": "Professor virtual",
            "provedor": preferred_provider,
            "modelo": preferred_model,
            "instrucoes": "Você é um professor paciente e didático.\nAdapte explicações ao nível do aluno.\nUse exemplos práticos e exercícios.\nSempre verifique se o aluno entendeu.",
            "ferramentas": ["Calculator", "DuckDuckGo"],
            "nivel": 1
        },
        "💼 Assistente de Vendas": {
            "nome": "Assistente de Vendas",
            "papel": "Especialista em vendas",
            "provedor": preferred_provider,
            "modelo": preferred_model,
            "instrucoes": "Você é um vendedor experiente e ético.\nFoque na satisfação do cliente.\nSeja persuasivo mas honesto.\nEntenda as necessidades antes de vender.",
            "ferramentas": ["Calculator", "DuckDuckGo"],
            "nivel": 1
        },
        "🎨 Assistente Criativo": {
            "nome": "Assistente Criativo",
            "papel": "Especialista em criação de conteúdo",
            "provedor": preferred_provider,
            "modelo": preferred_model,
            "instrucoes": "Você é um criativo experiente.\nCrie conteúdo original e envolvente.\nAdapte o tom e estilo ao público-alvo.\nSeja inovador e inspirador.",
            "ferramentas": ["DuckDuckGo", "Calculator"],
            "nivel": 1
        }
    }

def get_level_name(nivel):
    """Retorna nome do nível"""
    nomes = {
        1: "Ferramentas & Instruções",
        2: "Conhecimento & RAG",
        3: "Memória & Raciocínio", 
        4: "Times de Agentes",
        5: "Workflows Agênticos"
    }
    return nomes.get(nivel, "Desconhecido")

def get_level_description(nivel):
    """Retorna descrição do nível"""
    descricoes = {
        1: "Agentes básicos com ferramentas específicas e instruções personalizadas.",
        2: "Agentes com base de conhecimento (RAG) para consultar documentos.",
        3: "Agentes com memória persistente e capacidade de raciocínio.",
        4: "Múltiplos agentes trabalhando em equipe.",
        5: "Fluxos de trabalho complexos com estado e controle."
    }
    return descricoes.get(nivel, "Nível não definido")

def get_model_options(provedor):
    """Retorna opções de modelo por provedor"""
    modelos = {
        "OpenAI": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
        "Anthropic": ["claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"],
        "Google Gemini": ["gemini-2.0-flash-001", "gemini-1.5-pro", "gemini-1.5-flash"],
        "OpenRouter": ["openai/gpt-4o", "anthropic/claude-3-5-sonnet", "meta-llama/llama-3.1-8b-instruct:free"]
    }
    return modelos.get(provedor, ["modelo-padrao"])

def gerar_codigo(config):
    """Gera código Python para o agente"""
    
    # Imports
    imports = ["from agno.agent import Agent"]
    
    if config['provedor'] == "OpenAI":
        imports.append("from agno.models.openai import OpenAIChat")
        model_class = "OpenAIChat"
    elif config['provedor'] == "Anthropic":
        imports.append("from agno.models.anthropic import Claude")
        model_class = "Claude"
    elif config['provedor'] == "Google Gemini":
        imports.append("from agno.models.google import Gemini")
        model_class = "Gemini"
    elif config['provedor'] == "OpenRouter":
        imports.append("from agno.models.openrouter import OpenRouter")
        model_class = "OpenRouter"
    else:
        model_class = "OpenAIChat"
    
    # Imports de ferramentas
    tool_imports = {
        "DuckDuckGo": "from agno.tools.duckduckgo import DuckDuckGoTools",
        "Calculator": "from agno.tools.calculator import CalculatorTools",
        "YFinance": "from agno.tools.yfinance import YFinanceTools",
        "Email": "from agno.tools.email import EmailTools",
        "Python": "from agno.tools.python import PythonTools"
    }
    
    for ferramenta in config['ferramentas']:
        if ferramenta in tool_imports:
            imports.append(tool_imports[ferramenta])
    
    # Gerar código
    codigo = "\n".join(imports) + "\n\n"
    
    # Comentário sobre API
    if config['provedor'] == "OpenAI":
        codigo += "# Configure: export OPENAI_API_KEY=sua_chave\n\n"
    elif config['provedor'] == "Anthropic":
        codigo += "# Configure: export ANTHROPIC_API_KEY=sua_chave\n\n"
    elif config['provedor'] == "Google Gemini":
        codigo += "# Configure: export GOOGLE_API_KEY=sua_chave\n\n"
    elif config['provedor'] == "OpenRouter":
        codigo += "# Configure: export OPENROUTER_API_KEY=sua_chave\n\n"
    
    # Criar agente
    nome_var = config['nome'].lower().replace(' ', '_')
    codigo += f"""# Criar {config['nome']}
{nome_var} = Agent(
    name="{config['nome']}",
    role="{config['papel']}",
    model={model_class}(id="{config['modelo']}"),"""
    
    # Adicionar ferramentas
    if config['ferramentas']:
        codigo += "\n    tools=[\n"
        tool_classes = {
            "DuckDuckGo": "DuckDuckGoTools()",
            "Calculator": "CalculatorTools()",
            "YFinance": "YFinanceTools(stock_price=True)",
            "Email": "EmailTools()",
            "Python": "PythonTools()"
        }
        
        for ferramenta in config['ferramentas']:
            if ferramenta in tool_classes:
                codigo += f"        {tool_classes[ferramenta]},\n"
        codigo += "    ],"
    
    # Instruções
    instrucoes_linhas = config['instrucoes'].split('\n')
    codigo += '\n    instructions=[\n'
    for linha in instrucoes_linhas:
        if linha.strip():
            codigo += f'        "{linha.strip()}",\n'
    codigo += '    ],'
    
    # Configurações finais
    codigo += """
    show_tool_calls=True,
    markdown=True,
)

# Testar o agente
"""
    codigo += f'{nome_var}.print_response("Olá! Como você pode me ajudar?")\n'
    
    return codigo

def render_settings_tab():
    """Renderiza a aba de configurações"""
    import os
    
    st.header("⚙️ Configurações de API")
    st.markdown("Configure e teste suas chaves de API dos provedores de modelos.")
    
    # Inicializar session state para as chaves
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = get_env_vars()
    
    # Seção de configuração
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔑 Configurar Chaves de API")
        st.info("💡 As chaves são carregadas do arquivo .env e salvas automaticamente quando alteradas.")
        
        # OpenAI/OpenRouter
        st.markdown("### 🔵 OpenAI / OpenRouter")
        st.caption("Para OpenRouter, use OPENAI_API_KEY com sua chave do OpenRouter")
        
        current_openai = st.session_state.api_keys.get('OPENAI_API_KEY', '')
        openai_key = st.text_input(
            "OpenAI API Key:",
            value=current_openai,
            type="password",
            help="Para OpenAI: sk-proj-... | Para OpenRouter: sk-or-v1-...",
            key="openai_input"
        )
        
        # Detectar se é OpenRouter
        if openai_key.startswith('sk-or-v1-'):
            st.success("🌐 Chave do OpenRouter detectada!")
        elif openai_key.startswith('sk-proj-') or openai_key.startswith('sk-'):
            st.success("🔵 Chave do OpenAI detectada!")
        
        # OpenRouter específico
        st.markdown("### 🌐 OpenRouter (Opcional)")
        st.caption("Use apenas se quiser separar OpenRouter do OpenAI")
        
        current_openrouter = st.session_state.api_keys.get('OPENROUTER_API_KEY', '')
        openrouter_key = st.text_input(
            "OpenRouter API Key:",
            value=current_openrouter,
            type="password",
            help="Obtenha em: https://openrouter.ai/keys",
            key="openrouter_input"
        )
        
        # Anthropic
        st.markdown("### 🟠 Anthropic")
        current_anthropic = st.session_state.api_keys.get('ANTHROPIC_API_KEY', '')
        anthropic_key = st.text_input(
            "Anthropic API Key:",
            value=current_anthropic,
            type="password",
            help="Obtenha em: https://console.anthropic.com/",
            key="anthropic_input"
        )
        
        # Google
        st.markdown("### 🔴 Google Gemini")
        current_google = st.session_state.api_keys.get('GOOGLE_API_KEY', '')
        google_key = st.text_input(
            "Google API Key:",
            value=current_google,
            type="password",
            help="Obtenha em: https://makersuite.google.com/app/apikey",
            key="google_input"
        )
        
        # Botão para salvar todas as chaves
        st.markdown("---")
        col_save1, col_save2 = st.columns(2)
        
        with col_save1:
            if st.button("💾 Salvar Todas as Chaves", type="primary"):
                # Atualizar session state
                st.session_state.api_keys.update({
                    'OPENAI_API_KEY': openai_key,
                    'OPENROUTER_API_KEY': openrouter_key,
                    'ANTHROPIC_API_KEY': anthropic_key,
                    'GOOGLE_API_KEY': google_key
                })
                
                # Salvar no arquivo .env
                if save_env_file(st.session_state.api_keys):
                    st.success("✅ Chaves salvas no arquivo .env!")
                    st.info("🔄 As chaves foram atualizadas permanentemente")
                    
                    # Recarregar a página para aplicar as mudanças
                    st.rerun()
                else:
                    st.error("❌ Erro ao salvar no arquivo .env")
        
        with col_save2:
            if st.button("🔄 Recarregar do .env"):
                # Recarregar do arquivo
                env_data = load_env_file()
                st.session_state.api_keys = get_env_vars()
                st.success("✅ Chaves recarregadas do arquivo .env!")
                st.rerun()
    
    with col2:
        st.subheader("📊 Status das Chaves")
        
        # Mostrar status das chaves carregadas do .env
        st.markdown("#### 📁 Carregadas do arquivo .env:")
        env_vars = get_env_vars()
        
        for key, value in env_vars.items():
            provider_name = key.replace('_API_KEY', '').replace('_', ' ').title()
            if value:
                # Mostrar apenas os primeiros e últimos caracteres
                masked_key = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***"
                st.success(f"✅ {provider_name}: {masked_key}")
            else:
                st.error(f"❌ {provider_name}: Não configurado")
        
        st.markdown("---")
        st.subheader("🧪 Testar Conexões")
        
        # Status das APIs
        api_status = check_api_status()
        
        for provider, status in api_status.items():
            if status["configured"]:
                if st.button(f"🧪 Testar {provider}", key=f"test_{provider.lower()}"):
                    with st.spinner(f"Testando {provider}..."):
                        result = test_api_connection(provider)
                        if result["success"]:
                            st.success(f"✅ {provider}: {result['message']}")
                        else:
                            st.error(f"❌ {provider}: {result['error']}")
            else:
                st.warning(f"⚠️ {provider}: Chave não configurada")
        
        # Teste completo
        st.markdown("---")
        if st.button("🚀 Testar Todas as APIs", type="primary"):
            test_all_apis()
        
        # Informações sobre o arquivo .env
        st.markdown("---")
        st.subheader("📄 Arquivo .env")
        
        env_path = Path(".env")
        if env_path.exists():
            st.success("✅ Arquivo .env encontrado")
            
            # Mostrar localização do arquivo
            st.code(f"Localização: {env_path.absolute()}")
            
            # Botão para visualizar conteúdo (mascarado)
            if st.button("👁️ Visualizar .env (mascarado)"):
                try:
                    with open(env_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Mascarar chaves sensíveis
                    import re
                    masked_content = re.sub(
                        r'(API_KEY=)([^#\n]+)',
                        lambda m: f"{m.group(1)}{m.group(2)[:8]}...{m.group(2)[-4:]}" if len(m.group(2)) > 12 else f"{m.group(1)}***",
                        content
                    )
                    
                    st.code(masked_content, language="bash")
                except Exception as e:
                    st.error(f"Erro ao ler arquivo: {e}")
        else:
            st.warning("⚠️ Arquivo .env não encontrado")
            if st.button("📝 Criar arquivo .env"):
                save_env_file({})
                st.success("✅ Arquivo .env criado!")
                st.rerun()

def render_api_status_sidebar():
    """Renderiza status das APIs na barra lateral"""
    api_status = check_api_status()
    
    for provider, status in api_status.items():
        if status["configured"]:
            st.sidebar.success(f"✅ {provider}")
        else:
            st.sidebar.error(f"❌ {provider}")

def check_api_status():
    """Verifica status das chaves de API"""
    import os
    
    return {
        "OpenAI": {
            "configured": bool(os.getenv("OPENAI_API_KEY")),
            "key": os.getenv("OPENAI_API_KEY", "")[:20] + "..." if os.getenv("OPENAI_API_KEY") else ""
        },
        "Anthropic": {
            "configured": bool(os.getenv("ANTHROPIC_API_KEY")),
            "key": os.getenv("ANTHROPIC_API_KEY", "")[:20] + "..." if os.getenv("ANTHROPIC_API_KEY") else ""
        },
        "Google": {
            "configured": bool(os.getenv("GOOGLE_API_KEY")),
            "key": os.getenv("GOOGLE_API_KEY", "")[:20] + "..." if os.getenv("GOOGLE_API_KEY") else ""
        },
        "OpenRouter": {
            "configured": bool(os.getenv("OPENROUTER_API_KEY")),
            "key": os.getenv("OPENROUTER_API_KEY", "")[:20] + "..." if os.getenv("OPENROUTER_API_KEY") else ""
        }
    }

def test_api_connection(provider):
    """Testa conexão com um provedor específico"""
    try:
        if provider == "OpenAI":
            from agno.models.openai import OpenAIChat
            from agno.agent import Agent
            
            agent = Agent(
                model=OpenAIChat(id="gpt-3.5-turbo"),
                instructions=["Responda apenas 'OK' se conseguir me ouvir."]
            )
            
            response = agent.run("Teste de conexão")
            return {"success": True, "message": "Conexão estabelecida com sucesso!"}
            
        elif provider == "Anthropic":
            from agno.models.anthropic import Claude
            from agno.agent import Agent
            
            agent = Agent(
                model=Claude(id="claude-3-haiku"),
                instructions=["Responda apenas 'OK' se conseguir me ouvir."]
            )
            
            response = agent.run("Teste de conexão")
            return {"success": True, "message": "Conexão estabelecida com sucesso!"}
            
        elif provider == "Google":
            from agno.models.google import Gemini
            from agno.agent import Agent
            
            agent = Agent(
                model=Gemini(id="gemini-1.5-flash"),
                instructions=["Responda apenas 'OK' se conseguir me ouvir."]
            )
            
            response = agent.run("Teste de conexão")
            return {"success": True, "message": "Conexão estabelecida com sucesso!"}
            
        elif provider == "OpenRouter":
            from agno.models.openrouter import OpenRouter
            from agno.agent import Agent
            
            agent = Agent(
                model=OpenRouter(id="meta-llama/llama-3.1-8b-instruct:free"),
                instructions=["Responda apenas 'OK' se conseguir me ouvir."]
            )
            
            response = agent.run("Teste de conexão")
            return {"success": True, "message": "Conexão estabelecida com sucesso!"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

def test_all_apis():
    """Testa todas as APIs configuradas"""
    api_status = check_api_status()
    
    results = {}
    for provider, status in api_status.items():
        if status["configured"]:
            with st.spinner(f"Testando {provider}..."):
                result = test_api_connection(provider)
                results[provider] = result
    
    # Mostrar resultados
    st.subheader("📊 Resultados dos Testes")
    
    success_count = 0
    for provider, result in results.items():
        if result["success"]:
            st.success(f"✅ {provider}: {result['message']}")
            success_count += 1
        else:
            st.error(f"❌ {provider}: {result['error']}")
    
    if success_count == len(results):
        st.balloons()
        st.success(f"🎉 Todas as {success_count} APIs testadas com sucesso!")
    else:
        st.warning(f"⚠️ {success_count}/{len(results)} APIs funcionando corretamente")

if __name__ == "__main__":
    main()