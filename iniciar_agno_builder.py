#!/usr/bin/env python3
"""
Script de inicialização para o Agno Agent Builder
Versão simplificada e robusta para evitar problemas de contexto
"""

import streamlit as st
import sys
import os

# Adicionar o diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Função principal simplificada"""
    
    # Configurar página (apenas uma vez)
    try:
        st.set_page_config(
            page_title="🤖 Agno Agent Builder",
            page_icon="🤖",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        pass  # Página já configurada
    
    # Verificar se o Agno está disponível
    try:
        from agno.agent import Agent
        from agno.models.openai import OpenAIChat
        from agno.models.anthropic import Claude
        from agno.models.openrouter import OpenRouter
        from agno.models.google import Gemini
        AGNO_AVAILABLE = True
    except ImportError as e:
        st.error(f"""
        ❌ **Agno Framework não está instalado ou configurado corretamente**
        
        **Erro:** {e}
        
        **Para corrigir:**
        1. Instale o Agno: `pip install agno`
        2. Instale dependências: `pip install openai anthropic google-generativeai`
        3. Configure as chaves de API necessárias
        
        **Chaves de API:**
        - `export OPENAI_API_KEY=sua_chave`
        - `export ANTHROPIC_API_KEY=sua_chave`  
        - `export GOOGLE_API_KEY=sua_chave`
        - `export OPENROUTER_API_KEY=sua_chave`
        """)
        st.stop()
        return
    
    # Importar e executar o builder
    try:
        from agno_builder_interface import AgnoAgentBuilder
        
        # Criar e executar o builder
        builder = AgnoAgentBuilder()
        builder.run()
        
    except Exception as e:
        st.error(f"""
        ❌ **Erro ao inicializar o Agno Builder**
        
        **Erro:** {e}
        
        **Possíveis soluções:**
        1. Verifique se todas as dependências estão instaladas
        2. Certifique-se de que está executando com: `streamlit run iniciar_agno_builder.py`
        3. Verifique se o arquivo `agno_builder_interface.py` está no mesmo diretório
        """)
        
        # Mostrar traceback completo em modo debug
        if st.checkbox("🔍 Mostrar detalhes técnicos"):
            import traceback
            st.code(traceback.format_exc())

if __name__ == "__main__":
    main()