#!/usr/bin/env python3
"""
Script de inicialização corrigido para o Agno Builder
Ativa o ambiente virtual e configura tudo automaticamente
"""

import os
import sys
import subprocess
from pathlib import Path

def ativar_ambiente_virtual():
    """Ativa o ambiente virtual se existir"""
    venv_path = Path(".venv")
    
    if not venv_path.exists():
        print("❌ Ambiente virtual .venv não encontrado")
        print("💡 Execute: python -m venv .venv")
        return False
    
    # No Windows, o executável do Python fica em Scripts
    if os.name == 'nt':
        python_exe = venv_path / "Scripts" / "python.exe"
        pip_exe = venv_path / "Scripts" / "pip.exe"
    else:
        python_exe = venv_path / "bin" / "python"
        pip_exe = venv_path / "bin" / "pip"
    
    if not python_exe.exists():
        print("❌ Python não encontrado no ambiente virtual")
        return False
    
    print(f"✅ Usando ambiente virtual: {venv_path}")
    return str(python_exe), str(pip_exe)

def configurar_protobuf():
    """Configura o protobuf para compatibilidade"""
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    print("✅ Protobuf configurado")

def carregar_env():
    """Carrega variáveis do arquivo .env"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    if value and not value.startswith('sua_'):
                        os.environ[key] = value
        print("✅ Arquivo .env carregado")
    else:
        print("⚠️ Arquivo .env não encontrado")

def verificar_dependencias(python_exe, pip_exe):
    """Verifica e instala dependências necessárias"""
    print("📦 Verificando dependências...")
    
    dependencias = [
        "streamlit",
        "openai", 
        "anthropic",
        "google-generativeai",
        "google-genai",
        "python-dotenv"
    ]
    
    for dep in dependencias:
        try:
            result = subprocess.run([python_exe, "-c", f"import {dep.replace('-', '_')}"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ {dep}")
            else:
                print(f"⚠️ Instalando {dep}...")
                subprocess.run([pip_exe, "install", dep], check=True, capture_output=True)
                print(f"✅ {dep} instalado")
        except:
            print(f"❌ Erro com {dep}")

def corrigir_protobuf(pip_exe):
    """Corrige versão do protobuf"""
    print("🔧 Corrigindo protobuf...")
    try:
        subprocess.run([pip_exe, "install", "protobuf==3.20.3", "--force-reinstall"], 
                      check=True, capture_output=True)
        print("✅ Protobuf corrigido")
    except:
        print("⚠️ Erro ao corrigir protobuf")

def testar_agno(python_exe):
    """Testa se o Agno está funcionando"""
    print("🧪 Testando Agno...")
    
    test_script = '''
import os
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"

try:
    import agno
    print("✅ Agno OK")
    
    from agno.models.google import Gemini
    print("✅ Gemini OK")
    
    from agno.models.openai import OpenAIChat
    print("✅ OpenAI OK")
    
    print("🎉 Tudo funcionando!")
except Exception as e:
    print(f"❌ Erro: {e}")
'''
    
    try:
        result = subprocess.run([python_exe, "-c", test_script], 
                              capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("Avisos:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def iniciar_streamlit(python_exe):
    """Inicia o Streamlit"""
    print("🚀 Iniciando Agno Builder...")
    
    # Escolher arquivo da interface
    if Path("agno_builder_simples.py").exists():
        script = "agno_builder_simples.py"
    elif Path("agno_builder_interface.py").exists():
        script = "agno_builder_interface.py"
    else:
        print("❌ Arquivo da interface não encontrado")
        return False
    
    print(f"📝 Executando: {script}")
    print(f"🌐 Interface será aberta em: http://localhost:8501")
    print(f"⏹️ Para parar, pressione Ctrl+C")
    print("=" * 60)
    
    try:
        # Executar Streamlit com o Python do ambiente virtual
        subprocess.run([python_exe, "-m", "streamlit", "run", script])
        return True
    except KeyboardInterrupt:
        print("\n👋 Interface encerrada")
        return True
    except Exception as e:
        print(f"❌ Erro ao iniciar Streamlit: {e}")
        return False

def main():
    """Função principal"""
    print("🤖 Agno Builder - Inicializador Corrigido")
    print("=" * 60)
    
    # 1. Ativar ambiente virtual
    venv_result = ativar_ambiente_virtual()
    if not venv_result:
        return
    
    python_exe, pip_exe = venv_result
    
    # 2. Configurar protobuf
    configurar_protobuf()
    
    # 3. Carregar .env
    carregar_env()
    
    # 4. Verificar dependências
    verificar_dependencias(python_exe, pip_exe)
    
    # 5. Corrigir protobuf
    corrigir_protobuf(pip_exe)
    
    # 6. Testar Agno
    if not testar_agno(python_exe):
        print("❌ Agno não está funcionando corretamente")
        return
    
    # 7. Iniciar interface
    print("\n" + "=" * 60)
    iniciar_streamlit(python_exe)

if __name__ == "__main__":
    main()