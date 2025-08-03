#!/usr/bin/env python3
"""
Utilitário para carregar variáveis de ambiente do arquivo .env
"""

import os
from pathlib import Path

def load_env_file(env_file=".env"):
    """
    Carrega variáveis de ambiente de um arquivo .env
    
    Args:
        env_file (str): Caminho para o arquivo .env
    """
    env_path = Path(env_file)
    
    if not env_path.exists():
        print(f"⚠️ Arquivo {env_file} não encontrado")
        print(f"💡 Copie o arquivo .env.example para .env e configure suas chaves")
        return False
    
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        loaded_vars = []
        for line in lines:
            line = line.strip()
            
            # Ignorar comentários e linhas vazias
            if not line or line.startswith('#'):
                continue
            
            # Processar variáveis no formato KEY=VALUE
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remover aspas se existirem
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Definir variável de ambiente apenas se não estiver vazia
                if value and not value.startswith('xxx'):
                    os.environ[key] = value
                    loaded_vars.append(key)
        
        if loaded_vars:
            print(f"✅ Carregadas {len(loaded_vars)} variáveis do arquivo {env_file}:")
            for var in loaded_vars:
                # Mostrar apenas os primeiros caracteres por segurança
                value = os.environ[var]
                masked_value = value[:10] + "..." if len(value) > 10 else value
                print(f"   {var}={masked_value}")
        else:
            print(f"⚠️ Nenhuma variável válida encontrada em {env_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar {env_file}: {e}")
        return False

def check_required_apis():
    """Verifica quais APIs estão configuradas"""
    apis = {
        "OpenAI": "OPENAI_API_KEY",
        "Anthropic": "ANTHROPIC_API_KEY", 
        "Google": "GOOGLE_API_KEY",
        "OpenRouter": "OPENROUTER_API_KEY"
    }
    
    print("\n🔍 Status das APIs:")
    configured = []
    missing = []
    
    for name, env_var in apis.items():
        if os.getenv(env_var):
            print(f"   ✅ {name}")
            configured.append(name)
        else:
            print(f"   ❌ {name}")
            missing.append(name)
    
    print(f"\n📊 Resumo: {len(configured)}/{len(apis)} APIs configuradas")
    
    if missing:
        print(f"\n💡 Para configurar as APIs faltantes:")
        for name in missing:
            env_var = apis[name]
            print(f"   export {env_var}=sua_chave_{name.lower()}")
    
    return configured, missing

def create_env_from_example():
    """Cria arquivo .env a partir do .env.example"""
    example_path = Path(".env.example")
    env_path = Path(".env")
    
    if not example_path.exists():
        print("❌ Arquivo .env.example não encontrado")
        return False
    
    if env_path.exists():
        response = input("⚠️ Arquivo .env já existe. Sobrescrever? (y/N): ")
        if response.lower() != 'y':
            print("❌ Operação cancelada")
            return False
    
    try:
        # Copiar conteúdo do exemplo
        with open(example_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        with open(env_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Arquivo .env criado a partir de .env.example")
        print(f"💡 Edite o arquivo .env e configure suas chaves de API")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False

def main():
    """Função principal"""
    print("🔧 Agno Builder - Configurador de Ambiente")
    print("=" * 50)
    
    # Verificar se .env existe
    if not Path(".env").exists():
        print("📁 Arquivo .env não encontrado")
        
        if Path(".env.example").exists():
            response = input("💡 Criar .env a partir do exemplo? (Y/n): ")
            if response.lower() != 'n':
                if create_env_from_example():
                    print("\n📝 Agora edite o arquivo .env com suas chaves de API")
                    return
        else:
            print("❌ Arquivo .env.example também não encontrado")
            return
    
    # Carregar variáveis
    if load_env_file():
        check_required_apis()
        print(f"\n🚀 Execute: streamlit run agno_builder_simples.py")
    else:
        print(f"\n💡 Configure o arquivo .env e tente novamente")

if __name__ == "__main__":
    main()