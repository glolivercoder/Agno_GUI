#!/usr/bin/env python3
"""
Script de inicialização completo para o Agno Agent Builder
Verifica dependências, carrega configurações e inicia a interface
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    required_packages = {
        'streamlit': 'streamlit',
        'agno': 'agno'
    }
    
    missing = []
    installed = []
    
    for package, pip_name in required_packages.items():
        try:
            __import__(package)
            installed.append(package)
            print(f"✅ {package}")
        except ImportError:
            missing.append(pip_name)
            print(f"❌ {package}")
    
    if missing:
        print(f"\n💡 Para instalar dependências faltantes:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def install_provider_dependencies():
    """Instala dependências dos provedores automaticamente"""
    provider_packages = {
        'openai': 'OpenAI',
        'anthropic': 'Anthropic',
        'google-generativeai': 'Google Gemini'
    }
    
    print(f"\n📦 Instalando dependências dos provedores...")
    
    for package, provider in provider_packages.items():
        try:
            # Tentar importar primeiro
            if package == 'google-generativeai':
                __import__('google.generativeai')
            else:
                __import__(package)
            print(f"✅ {provider} já instalado")
        except ImportError:
            print(f"⚠️ Instalando {provider}...")
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", package], 
                             check=True, capture_output=True)
                print(f"✅ {provider} instalado com sucesso")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar {provider}: {e}")

def check_optional_dependencies():
    """Verifica dependências opcionais dos provedores"""
    optional_packages = {
        'openai': 'OpenAI',
        'anthropic': 'Anthropic', 
        'google.generativeai': 'Google Gemini'
    }
    
    print(f"\n🔍 Verificando provedores:")
    available_providers = []
    
    for package, provider in optional_packages.items():
        try:
            __import__(package)
            available_providers.append(provider)
            print(f"✅ {provider}")
        except ImportError:
            print(f"❌ {provider} não disponível")
    
    return available_providers

def load_env_file():
    """Carrega variáveis do arquivo .env"""
    env_path = Path(".env")
    
    if not env_path.exists():
        print(f"⚠️ Arquivo .env não encontrado")
        
        # Verificar se existe .env.example
        example_path = Path(".env.example")
        if example_path.exists():
            print(f"💡 Copie .env.example para .env e configure suas chaves:")
            print(f"   cp .env.example .env")
        
        return {}
    
    try:
        loaded_vars = {}
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip().strip('"').strip("'")
                    
                    if value and not value.startswith('xxx'):
                        os.environ[key] = value
                        loaded_vars[key] = value
        
        if loaded_vars:
            print(f"✅ Carregadas {len(loaded_vars)} variáveis do .env")
        else:
            print(f"⚠️ Nenhuma variável válida encontrada no .env")
        
        return loaded_vars
        
    except Exception as e:
        print(f"❌ Erro ao carregar .env: {e}")
        return {}

def check_api_keys():
    """Verifica quais chaves de API estão configuradas"""
    api_keys = {
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY",
        "Google": "GOOGLE_API_KEY", 
        "OpenRouter": "OPENROUTER_API_KEY"
    }
    
    print(f"\n🔑 Status das chaves de API:")
    configured = []
    
    for provider, env_var in api_keys.items():
        if os.getenv(env_var):
            configured.append(provider)
            print(f"✅ {provider}")
        else:
            print(f"❌ {provider}")
    
    if not configured:
        print(f"\n💡 Configure pelo menos uma chave de API para usar a interface")
        print(f"   Você pode configurar na aba Settings da interface")
    
    return configured

def start_streamlit():
    """Inicia a aplicação Streamlit"""
    print(f"\n🚀 Iniciando Agno Agent Builder...")
    
    # Verificar qual arquivo usar
    if Path("agno_builder_simples.py").exists():
        script = "agno_builder_simples.py"
    elif Path("iniciar_agno_builder.py").exists():
        script = "iniciar_agno_builder.py"
    else:
        print(f"❌ Arquivo da interface não encontrado")
        return False
    
    try:
        # Executar Streamlit
        cmd = [sys.executable, "-m", "streamlit", "run", script, "--server.headless", "true"]
        
        print(f"📝 Executando: streamlit run {script}")
        print(f"🌐 A interface será aberta em: http://localhost:8501")
        print(f"⏹️ Para parar, pressione Ctrl+C")
        print(f"=" * 60)
        
        subprocess.run(cmd)
        return True
        
    except KeyboardInterrupt:
        print(f"\n👋 Interface encerrada pelo usuário")
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar Streamlit: {e}")
        return False

def main():
    """Função principal"""
    print("🤖 Agno Agent Builder - Inicializador")
    print("=" * 50)
    
    # Verificações
    if not check_python_version():
        return
    
    print(f"\n📦 Verificando dependências:")
    if not check_dependencies():
        return
    
    # Instalar e verificar provedores
    install_provider_dependencies()
    available_providers = check_optional_dependencies()
    
    # Carregar configurações
    print(f"\n⚙️ Carregando configurações:")
    env_vars = load_env_file()
    
    # Verificar APIs
    configured_apis = check_api_keys()
    
    # Resumo
    print(f"\n📊 Resumo:")
    print(f"   🐍 Python: OK")
    print(f"   📦 Dependências: OK")
    print(f"   🤖 Provedores: {len(available_providers)} disponíveis")
    print(f"   🔑 APIs: {len(configured_apis)} configuradas")
    
    if not configured_apis:
        print(f"\n⚠️ Nenhuma API configurada!")
        print(f"   Você pode configurar na aba Settings da interface")
        
        response = input(f"\n❓ Continuar mesmo assim? (Y/n): ")
        if response.lower() == 'n':
            print(f"👋 Configuração cancelada")
            return
    
    # Iniciar interface
    start_streamlit()

if __name__ == "__main__":
    main()