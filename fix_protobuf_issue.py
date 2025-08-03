#!/usr/bin/env python3
"""
Script para corrigir problemas de compatibilidade do protobuf com Streamlit
"""

import subprocess
import sys
import os

def fix_protobuf_compatibility():
    """Corrige problemas de compatibilidade do protobuf"""
    
    print("🔧 Corrigindo problemas de compatibilidade do protobuf...")
    
    # Método 1: Definir variável de ambiente
    print("\n1️⃣ Definindo variável de ambiente PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION")
    os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] = "python"
    
    # Método 2: Downgrade do protobuf
    print("\n2️⃣ Fazendo downgrade do protobuf para versão compatível")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "protobuf==3.20.3", "--force-reinstall"
        ], check=True)
        print("✅ Protobuf downgrade realizado com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no downgrade do protobuf: {e}")
    
    # Método 3: Atualizar streamlit
    print("\n3️⃣ Atualizando Streamlit para versão mais recente")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "streamlit", "--upgrade"
        ], check=True)
        print("✅ Streamlit atualizado com sucesso")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro na atualização do Streamlit: {e}")
    
    print("\n✅ Correções aplicadas!")
    print("💡 Tente executar novamente: streamlit run agno_builder_simples.py")

def check_versions():
    """Verifica versões dos pacotes problemáticos"""
    packages = ['streamlit', 'protobuf', 'agno']
    
    print("📦 Versões dos pacotes:")
    for package in packages:
        try:
            result = subprocess.run([
                sys.executable, "-c", f"import {package}; print({package}.__version__)"
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ {package}: {version}")
            else:
                print(f"   ❌ {package}: não instalado")
        except Exception as e:
            print(f"   ❌ {package}: erro ao verificar - {e}")

def main():
    print("🚨 Agno Builder - Corretor de Problemas")
    print("=" * 50)
    
    print("📊 Verificando versões atuais:")
    check_versions()
    
    print("\n" + "=" * 50)
    response = input("🔧 Aplicar correções? (Y/n): ")
    
    if response.lower() != 'n':
        fix_protobuf_compatibility()
        
        print("\n" + "=" * 50)
        print("📊 Verificando versões após correção:")
        check_versions()
    else:
        print("❌ Correções canceladas")

if __name__ == "__main__":
    main()