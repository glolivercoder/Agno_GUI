#!/usr/bin/env python3
"""
Agno Agent Builder - Versão Simplificada
Interface gráfica básica para criar agentes Agno sem problemas de contexto
"""

import streamlit as st
import json
import os
from datetime import datetime
from pathlib import Path

# Carregar variáveis de ambiente do arquivo .env
def load_env_file():
    """Carrega variáveis do arquivo .env se existir"""
    env_path = Path(".env")
    if env_path.exists():
        try:
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip().strip('"').strip("'")
                        if value and not value.startswith('xxx'):
                            os.environ[key] = value
            return True
        except Exception:
            pass
    return False

# Carregar .env no início
load_env_file()

# Configurar página
st.set_page_config(
    page_title="🤖 Agno Agent Builder",
    page_icon="🤖",
    layout="wide"
)

def main():
    """Interface principal simplificada"""
    
    # Título
    st.title("🤖 Agno Agent Builder")
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
    
    # Abas principais
    tab1, tab2 = st.tabs(["🛠️ Builder", "⚙️ Settings"])
    
    with tab1:
        render_builder_tab()
    
    with tab2:
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
    
    # Seção de configuração
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🔑 Configurar Chaves de API")
        
        # OpenAI
        st.markdown("### 🔵 OpenAI")
        openai_key = st.text_input(
            "OpenAI API Key:",
            value=os.getenv("OPENAI_API_KEY", ""),
            type="password",
            help="Obtenha em: https://platform.openai.com/api-keys"
        )
        
        if st.button("💾 Salvar OpenAI", key="save_openai"):
            os.environ["OPENAI_API_KEY"] = openai_key
            st.success("✅ Chave OpenAI salva temporariamente!")
        
        # Anthropic
        st.markdown("### 🟠 Anthropic")
        anthropic_key = st.text_input(
            "Anthropic API Key:",
            value=os.getenv("ANTHROPIC_API_KEY", ""),
            type="password",
            help="Obtenha em: https://console.anthropic.com/"
        )
        
        if st.button("💾 Salvar Anthropic", key="save_anthropic"):
            os.environ["ANTHROPIC_API_KEY"] = anthropic_key
            st.success("✅ Chave Anthropic salva temporariamente!")
        
        # Google
        st.markdown("### 🔴 Google Gemini")
        google_key = st.text_input(
            "Google API Key:",
            value=os.getenv("GOOGLE_API_KEY", ""),
            type="password",
            help="Obtenha em: https://makersuite.google.com/app/apikey"
        )
        
        if st.button("💾 Salvar Google", key="save_google"):
            os.environ["GOOGLE_API_KEY"] = google_key
            st.success("✅ Chave Google salva temporariamente!")
        
        # OpenRouter
        st.markdown("### 🌐 OpenRouter")
        openrouter_key = st.text_input(
            "OpenRouter API Key:",
            value=os.getenv("OPENROUTER_API_KEY", ""),
            type="password",
            help="Obtenha em: https://openrouter.ai/keys"
        )
        
        if st.button("💾 Salvar OpenRouter", key="save_openrouter"):
            os.environ["OPENROUTER_API_KEY"] = openrouter_key
            st.success("✅ Chave OpenRouter salva temporariamente!")
    
    with col2:
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
    
    # Seção de instruções
    st.markdown("---")
    st.subheader("📋 Instruções")
    
    with st.expander("💡 Como configurar as chaves de API"):
        st.markdown("""
        ### Método 1: Interface (Temporário)
        1. Cole suas chaves nos campos acima
        2. Clique em "Salvar" para cada provedor
        3. **Nota**: As chaves são salvas apenas durante esta sessão
        
        ### Método 2: Variáveis de Ambiente (Permanente)
        
        **Windows (PowerShell):**
        ```powershell
        $env:OPENAI_API_KEY="sua_chave_openai"
        $env:ANTHROPIC_API_KEY="sua_chave_anthropic"
        $env:GOOGLE_API_KEY="sua_chave_google"
        $env:OPENROUTER_API_KEY="sua_chave_openrouter"
        ```
        
        **Linux/Mac (Bash):**
        ```bash
        export OPENAI_API_KEY="sua_chave_openai"
        export ANTHROPIC_API_KEY="sua_chave_anthropic"
        export GOOGLE_API_KEY="sua_chave_google"
        export OPENROUTER_API_KEY="sua_chave_openrouter"
        ```
        
        ### Método 3: Arquivo .env
        1. Copie o arquivo `.env.example` para `.env`
        2. Edite o arquivo `.env` com suas chaves
        3. Reinicie a aplicação
        """)
    
    with st.expander("🔗 Links para obter chaves de API"):
        st.markdown("""
        - **OpenAI**: https://platform.openai.com/api-keys
        - **Anthropic**: https://console.anthropic.com/
        - **Google Gemini**: https://makersuite.google.com/app/apikey
        - **OpenRouter**: https://openrouter.ai/keys
        
        ### Custos Aproximados:
        - **OpenAI**: $0.01-0.06 por 1K tokens
        - **Anthropic**: $0.015-0.075 por 1K tokens
        - **Google**: Gratuito até 15 req/min, depois $0.001-0.002 por 1K tokens
        - **OpenRouter**: Varia por modelo (muitos gratuitos disponíveis)
        """)

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