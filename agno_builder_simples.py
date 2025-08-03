#!/usr/bin/env python3
"""
Agno Agent Builder - Versão Simplificada
Interface gráfica básica para criar agentes Agno sem problemas de contexto
"""

import streamlit as st
import json
from datetime import datetime

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
        st.success("✅ Agno Framework carregado com sucesso!")
    except ImportError as e:
        st.error(f"""
        ❌ **Agno não está instalado**
        
        **Instale com:** `pip install agno`
        
        **Erro:** {e}
        """)
        return
    
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

if __name__ == "__main__":
    main()