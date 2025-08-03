#!/usr/bin/env python3
"""
Script para corrigir problemas de instalação do Agno
"""

import os
import sys
import subprocess
from pathlib import Path

def executar_comando(comando, descricao=""):
    """Executa um comando e mostra o resultado"""
    if descricao:
        print(f"🔧 {descricao}...")
    
    try:
        result = subprocess.run(comando, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {descricao or 'Comando'} executado com sucesso")
            if result.stdout.strip():
                print(f"📝 {result.stdout.strip()}")
            return True
        else:
            print(f"❌ Erro em {descricao or 'comando'}")
            if result.stderr.strip():
                print(f"🚨 {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ Exceção em {descricao}: {e}")
        return False

def verificar_ambiente_virtual():
    """Verifica se estamos no ambiente virtual"""
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("❌ Ambiente virtual .venv não encontrado")
        print("💡 Criando ambiente virtual...")
        if executar_comando("python -m venv .venv", "Criando ambiente virtual"):
            print("✅ Ambiente virtual criado")
        else:
            return False
    
    # Verificar se estamos usando o ambiente virtual
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Ambiente virtual ativo")
        return True
    else:
        print("⚠️ Ambiente virtual não está ativo")
        print("💡 Ative com: .venv\\Scripts\\activate (Windows) ou source .venv/bin/activate (Linux/Mac)")
        return False

def instalar_agno():
    """Instala o Agno Framework"""
    print("📦 Instalando Agno Framework...")
    
    # Primeiro, instalar dependências básicas
    dependencias_basicas = [
        "pip --upgrade",
        "setuptools",
        "wheel"
    ]
    
    for dep in dependencias_basicas:
        executar_comando(f"pip install {dep}", f"Instalando {dep}")
    
    # Instalar Agno
    if executar_comando("pip install -U agno", "Instalando Agno"):
        print("✅ Agno instalado")
        return True
    else:
        print("❌ Falha ao instalar Agno")
        return False

def instalar_dependencias_modelos():
    """Instala dependências dos modelos de IA"""
    print("🤖 Instalando dependências dos modelos...")
    
    dependencias = [
        "openai",
        "anthropic", 
        "google-generativeai",
        "google-genai",
        "streamlit",
        "python-dotenv"
    ]
    
    sucesso = True
    for dep in dependencias:
        if not executar_comando(f"pip install {dep}", f"Instalando {dep}"):
            sucesso = False
    
    return sucesso

def corrigir_protobuf():
    """Corrige problemas do protobuf"""
    print("🔧 Corrigindo protobuf...")
    
    # Definir variável de ambiente
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    
    # Fazer downgrade do protobuf
    if executar_comando("pip install protobuf==3.20.3 --force-reinstall", "Corrigindo protobuf"):
        print("✅ Protobuf corrigido")
        return True
    else:
        print("❌ Falha ao corrigir protobuf")
        return False

def testar_importacoes():
    """Testa se as importações estão funcionando"""
    print("🧪 Testando importações...")
    
    testes = [
        ("agno", "import agno; print('Agno:', agno.__version__)"),
        ("OpenAI", "from agno.models.openai import OpenAIChat; print('OpenAI: OK')"),
        ("Anthropic", "from agno.models.anthropic import Claude; print('Anthropic: OK')"),
        ("Google Gemini", "from agno.models.google import Gemini; print('Gemini: OK')"),
        ("Streamlit", "import streamlit; print('Streamlit:', streamlit.__version__)")
    ]
    
    sucessos = 0
    for nome, codigo in testes:
        try:
            result = subprocess.run([sys.executable, "-c", codigo], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {nome}: {result.stdout.strip()}")
                sucessos += 1
            else:
                print(f"❌ {nome}: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ {nome}: Erro - {e}")
    
    print(f"📊 Resultado: {sucessos}/{len(testes)} testes passaram")
    return sucessos == len(testes)

def criar_arquivo_env():
    """Cria arquivo .env se não existir"""
    env_file = Path(".env")
    if not env_file.exists():
        print("📝 Criando arquivo .env...")
        
        conteudo_env = """# Agno Agent Builder - Configuração de APIs
# Configure suas chaves de API aqui

# OpenAI - https://platform.openai.com/api-keys
OPENAI_API_KEY=

# Anthropic - https://console.anthropic.com/
ANTHROPIC_API_KEY=

# Google Gemini - https://makersuite.google.com/app/apikey
GOOGLE_API_KEY=

# OpenRouter - https://openrouter.ai/keys
OPENROUTER_API_KEY=

# Configuração do protobuf para compatibilidade
PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
"""
        
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(conteudo_env)
        
        print("✅ Arquivo .env criado")
        print("💡 Edite o arquivo .env para adicionar suas chaves de API")
    else:
        print("✅ Arquivo .env já existe")

def mostrar_instrucoes():
    """Mostra instruções finais"""
    print("\n" + "=" * 60)
    print("🎉 Correção Concluída!")
    print("=" * 60)
    
    print("\n📋 Próximos Passos:")
    print("1. Configure suas chaves de API no arquivo .env")
    print("2. Execute: python iniciar_agno_corrigido.py")
    print("3. Ou execute diretamente: streamlit run agno_builder_simples.py")
    
    print("\n🔑 Para obter chaves de API:")
    print("• Google Gemini: https://makersuite.google.com/app/apikey")
    print("• OpenRouter: https://openrouter.ai/keys")
    print("• OpenAI: https://platform.openai.com/api-keys")
    print("• Anthropic: https://console.anthropic.com/")
    
    print("\n💡 Dicas:")
    print("• OpenRouter tem modelos gratuitos!")
    print("• Google Gemini tem cota gratuita generosa")
    print("• Sempre ative o ambiente virtual antes de usar")

def main():
    """Função principal"""
    print("🔧 Corretor de Instalação do Agno Builder")
    print("=" * 60)
    
    # 1. Verificar ambiente virtual
    if not verificar_ambiente_virtual():
        print("❌ Configure o ambiente virtual primeiro")
        return
    
    # 2. Instalar Agno
    if not instalar_agno():
        print("❌ Falha na instalação do Agno")
        return
    
    # 3. Instalar dependências dos modelos
    if not instalar_dependencias_modelos():
        print("⚠️ Algumas dependências falharam, mas continuando...")
    
    # 4. Corrigir protobuf
    corrigir_protobuf()
    
    # 5. Testar importações
    if testar_importacoes():
        print("✅ Todas as importações funcionando!")
    else:
        print("⚠️ Algumas importações falharam")
    
    # 6. Criar arquivo .env
    criar_arquivo_env()
    
    # 7. Mostrar instruções
    mostrar_instrucoes()

if __name__ == "__main__":
    main()