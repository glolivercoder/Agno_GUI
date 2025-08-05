#!/usr/bin/env python3
"""
Script de inicialização para a versão corrigida do Agno Builder
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Inicia a versão corrigida do Agno Builder"""
    print("🤖 Iniciando Agno Builder - Versão Corrigida")
    print("=" * 50)
    
    # Configurar protobuf
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    print("✅ Protobuf configurado")
    
    # Verificar se estamos no ambiente virtual
    venv_path = Path(".venv")
    if venv_path.exists():
        if os.name == 'nt':  # Windows
            python_exe = venv_path / "Scripts" / "python.exe"
            streamlit_exe = venv_path / "Scripts" / "streamlit.exe"
        else:  # Linux/Mac
            python_exe = venv_path / "bin" / "python"
            streamlit_exe = venv_path / "bin" / "streamlit"
        
        if python_exe.exists():
            print("✅ Usando ambiente virtual")
            cmd = [str(streamlit_exe), "run", "agno_builder_corrigido.py"]
        else:
            print("⚠️ Ambiente virtual encontrado mas Python não localizado")
            cmd = [sys.executable, "-m", "streamlit", "run", "agno_builder_corrigido.py"]
    else:
        print("⚠️ Ambiente virtual não encontrado, usando Python do sistema")
        cmd = [sys.executable, "-m", "streamlit", "run", "agno_builder_corrigido.py"]
    
    print(f"🚀 Executando: {' '.join(cmd)}")
    print("🌐 Interface será aberta em: http://localhost:8501")
    print("⏹️ Para parar, pressione Ctrl+C")
    print("=" * 50)
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Agno Builder encerrado")
    except Exception as e:
        print(f"❌ Erro: {e}")

if __name__ == "__main__":
    main()