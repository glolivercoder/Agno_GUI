#!/usr/bin/env python3
"""
Componente de filtros para modelos do OpenRouter
"""

import streamlit as st
from typing import List, Set, Tuple, Optional
from openrouter_api import OpenRouterModel, get_openrouter_models
import os

class OpenRouterFilters:
    """Componente de filtros para modelos do OpenRouter"""
    
    def __init__(self):
        self.models: List[OpenRouterModel] = []
        self.filtered_models: List[OpenRouterModel] = []
        self.companies: Set[str] = set()
    
    def load_models(self, api_key: Optional[str] = None) -> bool:
        """
        Carrega modelos do OpenRouter
        
        Args:
            api_key: Chave da API (opcional)
            
        Returns:
            True se carregou com sucesso
        """
        try:
            with st.spinner("🔄 Carregando modelos do OpenRouter..."):
                self.models = get_openrouter_models(api_key=api_key, use_cache=True)
                self.companies = set(model.company for model in self.models)
                self.filtered_models = self.models.copy()
            return True
        except Exception as e:
            st.error(f"❌ Erro ao carregar modelos: {e}")
            return False
    
    def render_filters(self) -> Tuple[str, str, bool, bool]:
        """
        Renderiza os filtros na interface
        
        Returns:
            Tupla com (search_query, selected_company, show_only_free, show_only_paid)
        """
        # Container para filtros
        with st.container():
            # Linha 1: Busca e empresa
            col1, col2 = st.columns([2, 1])
            
            with col1:
                search_query = st.text_input(
                    "🔍 Buscar modelo",
                    placeholder="Digite o nome do modelo...",
                    help="Busque por nome do modelo ou ID"
                )
            
            with col2:
                companies_list = ["Todas"] + sorted(list(self.companies))
                selected_company = st.selectbox(
                    "🏢 Empresa",
                    companies_list,
                    help="Filtrar por empresa/provedor"
                )
            
            # Linha 2: Filtros de preço e estatísticas
            col3, col4, col5 = st.columns([1, 1, 2])
            
            with col3:
                show_only_free = st.checkbox(
                    "🆓 Apenas gratuitos",
                    help="Mostrar apenas modelos gratuitos"
                )
            
            with col4:
                show_only_paid = st.checkbox(
                    "💰 Apenas pagos",
                    help="Mostrar apenas modelos pagos"
                )
            
            with col5:
                # Mostrar estatísticas
                if self.models:
                    total = len(self.models)
                    free_count = len([m for m in self.models if m.is_free])
                    paid_count = total - free_count
                    
                    st.info(f"📊 Total: {total} | 🆓 Gratuitos: {free_count} | 💰 Pagos: {paid_count}")
        
        return search_query, selected_company, show_only_free, show_only_paid
    
    def apply_filters(self, search_query: str, selected_company: str, 
                     show_only_free: bool, show_only_paid: bool) -> List[OpenRouterModel]:
        """
        Aplica filtros aos modelos
        
        Args:
            search_query: Texto de busca
            selected_company: Empresa selecionada
            show_only_free: Mostrar apenas gratuitos
            show_only_paid: Mostrar apenas pagos
            
        Returns:
            Lista de modelos filtrados
        """
        filtered = self.models.copy()
        
        # Filtro de busca
        if search_query.strip():
            query_lower = search_query.lower().strip()
            filtered = [
                model for model in filtered
                if (query_lower in model.name.lower() or 
                    query_lower in model.id.lower() or
                    query_lower in model.company.lower())
            ]
        
        # Filtro por empresa
        if selected_company != "Todas":
            filtered = [
                model for model in filtered
                if model.company == selected_company
            ]
        
        # Filtros de preço
        if show_only_free and show_only_paid:
            # Se ambos marcados, mostrar todos (comportamento intuitivo)
            pass
        elif show_only_free:
            filtered = [model for model in filtered if model.is_free]
        elif show_only_paid:
            filtered = [model for model in filtered if not model.is_free]
        
        self.filtered_models = filtered
        return filtered
    
    def render_model_card(self, model: OpenRouterModel) -> None:
        """
        Renderiza um card de modelo
        
        Args:
            model: Modelo para renderizar
        """
        with st.container():
            # Header do card
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                # Nome e empresa
                st.markdown(f"**{model.name}**")
                st.caption(f"🏢 {model.company} • `{model.id}`")
            
            with col2:
                # Indicador de preço
                if model.is_free:
                    st.success("🆓 GRATUITO")
                else:
                    st.warning("💰 PAGO")
            
            with col3:
                # Context length
                if model.context_length > 0:
                    if model.context_length >= 1000000:
                        ctx_str = f"{model.context_length/1000000:.1f}M"
                    elif model.context_length >= 1000:
                        ctx_str = f"{model.context_length/1000:.0f}K"
                    else:
                        ctx_str = str(model.context_length)
                    st.info(f"📝 {ctx_str}")
            
            # Informações de preço (se disponível)
            if not model.is_free and (model.price_input or model.price_output):
                price_info = []
                if model.price_input:
                    price_info.append(f"Entrada: ${model.price_input:.6f}")
                if model.price_output:
                    price_info.append(f"Saída: ${model.price_output:.6f}")
                
                if price_info:
                    st.caption(f"💵 {' | '.join(price_info)} por token")
            
            # Descrição (se disponível)
            if model.description:
                with st.expander("ℹ️ Descrição"):
                    st.write(model.description)
    
    def render_model_selector(self, models: List[OpenRouterModel]) -> Optional[str]:
        """
        Renderiza seletor de modelos
        
        Args:
            models: Lista de modelos filtrados
            
        Returns:
            ID do modelo selecionado ou None
        """
        if not models:
            st.warning("🔍 Nenhum modelo encontrado com os filtros aplicados")
            return None
        
        # Mostrar quantidade de resultados
        st.info(f"📋 {len(models)} modelo(s) encontrado(s)")
        
        # Opções para o selectbox
        model_options = []
        model_ids = []
        
        for model in models:
            # Criar label com informações importantes
            label = f"{model.name}"
            
            # Adicionar empresa se não estiver no nome
            if model.company.lower() not in model.name.lower():
                label += f" ({model.company})"
            
            # Adicionar indicadores
            if model.is_free:
                label += " 🆓"
            else:
                label += " 💰"
            
            # Adicionar context length se significativo
            if model.context_length >= 100000:
                if model.context_length >= 1000000:
                    label += f" [{model.context_length/1000000:.1f}M]"
                else:
                    label += f" [{model.context_length/1000:.0f}K]"
            
            model_options.append(label)
            model_ids.append(model.id)
        
        # Selectbox para escolher modelo
        selected_index = st.selectbox(
            "🤖 Selecionar Modelo:",
            range(len(model_options)),
            format_func=lambda x: model_options[x],
            help="Escolha o modelo que deseja usar"
        )
        
        if selected_index is not None:
            selected_model = models[selected_index]
            
            # Mostrar detalhes do modelo selecionado
            with st.expander("📋 Detalhes do modelo selecionado", expanded=True):
                self.render_model_card(selected_model)
            
            return model_ids[selected_index]
        
        return None
    
    def render_complete_interface(self, api_key: Optional[str] = None) -> Optional[str]:
        """
        Renderiza interface completa de seleção de modelos
        
        Args:
            api_key: Chave da API (opcional)
            
        Returns:
            ID do modelo selecionado ou None
        """
        # Carregar modelos se necessário
        if not self.models:
            if not self.load_models(api_key):
                return None
        
        # Botão para recarregar
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔄 Atualizar", help="Recarregar lista de modelos"):
                # Limpar cache e recarregar
                from openrouter_api import ModelCache
                cache = ModelCache()
                cache.clear_cache()
                self.models = []
                st.rerun()
        
        # Renderizar filtros
        search_query, selected_company, show_only_free, show_only_paid = self.render_filters()
        
        # Aplicar filtros
        filtered_models = self.apply_filters(search_query, selected_company, show_only_free, show_only_paid)
        
        # Renderizar seletor
        return self.render_model_selector(filtered_models)

def test_filters_component():
    """Testa o componente de filtros"""
    print("🧪 Testando componente de filtros...")
    
    # Simular Streamlit session state
    if not hasattr(st, 'session_state'):
        st.session_state = {}
    
    # Criar componente
    filters = OpenRouterFilters()
    
    # Carregar modelos (sem API key para usar fallback)
    success = filters.load_models(api_key=None)
    assert success, "Deveria carregar modelos com sucesso"
    
    print(f"✅ Carregados {len(filters.models)} modelos")
    print(f"✅ Encontradas {len(filters.companies)} empresas")
    
    # Testar filtros
    # Filtro por empresa
    openai_models = filters.apply_filters("", "Openai", False, False)
    print(f"✅ Modelos OpenAI: {len(openai_models)}")
    
    # Filtro por gratuitos
    free_models = filters.apply_filters("", "Todas", True, False)
    print(f"✅ Modelos gratuitos: {len(free_models)}")
    
    # Filtro por pagos
    paid_models = filters.apply_filters("", "Todas", False, True)
    print(f"✅ Modelos pagos: {len(paid_models)}")
    
    # Filtro de busca
    gpt_models = filters.apply_filters("gpt", "Todas", False, False)
    print(f"✅ Modelos com 'gpt': {len(gpt_models)}")
    
    print("🎉 Componente de filtros funcionando!")

if __name__ == "__main__":
    test_filters_component()