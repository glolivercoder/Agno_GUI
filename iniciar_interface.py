#!/usr/bin/env python3
"""
Script para iniciar a interface do Agno Builder
Ativa o ambiente virtual automaticamente e inicia o Streamlit
"""

import os
import sys
import subprocess
from pathlib import Path

def verificar_ambiente_virtual():
    """Verifica se estamos no ambiente virtual"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return True
    return False

def ativar_ambiente_virtual():
    """Ativa o ambiente virtual se necessário"""
    if verificar_ambiente_virtual():
        print("✅ Ambiente virtual já ativo")
        return True
    
    venv_path = Path(".venv")
    if not venv_path.exists():
        print("❌ Ambiente virtual .venv não encontrado")
        print("💡 Execute: python -m venv .venv")
        return False
    
    # No Windows, usar o executável do ambiente virtual
    if os.name == 'nt':
        python_exe = venv_path / "Scripts" / "python.exe"
        streamlit_exe = venv_path / "Scripts" / "streamlit.exe"
    else:
        python_exe = venv_path / "bin" / "python"
        streamlit_exe = venv_path / "bin" / "streamlit"
    
    if not python_exe.exists():
        print("❌ Python não encontrado no ambiente virtual")
        return False
    
    return str(python_exe), str(streamlit_exe)

def configurar_ambiente():
    """Configura variáveis de ambiente necessárias"""
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    print("✅ Protobuf configurado")

def iniciar_streamlit():
    """Inicia o Streamlit com a interface"""
    print("🚀 Iniciando Agno Builder...")
    
    # Verificar se arquivo existe
    interface_file = "agno_builder_interface.py"
    if not Path(interface_file).exists():
        print(f"❌ Arquivo {interface_file} não encontrado")
        return False
    
    try:
        # Se não estamos no ambiente virtual, usar executáveis específicos
        if not verificar_ambiente_virtual():
            executables = ativar_ambiente_virtual()
            if not executables:
                return False
            
            python_exe, streamlit_exe = executables
            
            # Executar streamlit com o Python do ambiente virtual
            cmd = [str(streamlit_exe), "run", interface_file]
        else:
            # Já estamos no ambiente virtual
            cmd = [sys.executable, "-m", "streamlit", "run", interface_file]
        
        print(f"📝 Executando: {' '.join(cmd)}")
        print(f"🌐 Interface será aberta em: http://localhost:8501")
        print(f"⏹️ Para parar, pressione Ctrl+C")
        print("=" * 60)
        
        # Executar comando
        subprocess.run(cmd)
        return True
        
    except KeyboardInterrupt:
        print("\n👋 Interface encerrada pelo usuário")
        return True
    except FileNotFoundError as e:
        print(f"❌ Comando não encontrado: {e}")
        print("💡 Certifique-se de que o Streamlit está instalado no ambiente virtual")
        return False
    except Exception as e:
        print(f"❌ Erro ao iniciar interface: {e}")
        return False

def main():
    """Função principal"""
    print("🤖 Agno Builder - Inicializador de Interface")
    print("=" * 60)
    
    # Configurar ambiente
    configurar_ambiente()
    
    # Verificar ambiente virtual
    if verificar_ambiente_virtual():
        print("✅ Ambiente virtual ativo")
    else:
        print("⚠️ Ambiente virtual não ativo - tentando usar .venv")
    
    # Iniciar interface
    success = iniciar_streamlit()
    
    if not success:
        print("\n❌ Falha ao iniciar interface")
        print("\n💡 Soluções:")
        print("1. Ative o ambiente virtual: .venv\\Scripts\\activate")
        print("2. Instale dependências: pip install streamlit agno")
        print("3. Execute manualmente: streamlit run agno_builder_interface.py")
        sys.exit(1)

if __name__ == "__main__":
    main()