#!/usr/bin/env python3
"""
Agno Agent Builder - Versão CLI (Command Line Interface)
Alternativa sem Streamlit para casos de problemas de compatibilidade
"""

import os
import json
from datetime import datetime
from pathlib import Path

class AgnoBuilderCLI:
    """Interface de linha de comando para criar agentes Agno"""
    
    def __init__(self):
        self.config = {}
        self.load_env()
    
    def load_env(self):
        """Carrega variáveis do arquivo .env"""
        env_path = Path(".env")
        if env_path.exists():
            try:
                with open(env_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip().strip('"').strip("'")
                            if value and not value.startswith('xxx'):
                                os.environ[key] = value
                print("✅ Arquivo .env carregado")
            except Exception as e:
                print(f"⚠️ Erro ao carregar .env: {e}")
    
    def check_agno(self):
        """Verifica se o Agno está disponível"""
        try:
            import agno
            from agno.agent import Agent
            from agno.models.openai import OpenAIChat
            from agno.models.anthropic import Claude
            print("✅ Agno Framework disponível")
            return True
        except ImportError as e:
            print(f"❌ Agno não disponível: {e}")
            print("💡 Instale com: pip install agno")
            return False
    
    def check_apis(self):
        """Verifica status das APIs"""
        apis = {
            "OpenAI": "OPENAI_API_KEY",
            "Anthropic": "ANTHROPIC_API_KEY",
            "Google": "GOOGLE_API_KEY",
            "OpenRouter": "OPENROUTER_API_KEY"
        }
        
        print("\n🔑 Status das APIs:")
        configured = []
        
        for name, env_var in apis.items():
            if os.getenv(env_var):
                print(f"   ✅ {name}")
                configured.append(name)
            else:
                print(f"   ❌ {name}")
        
        return configured
    
    def get_user_input(self, prompt, default=""):
        """Obtém entrada do usuário com valor padrão"""
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            return user_input if user_input else default
        else:
            return input(f"{prompt}: ").strip()
    
    def select_option(self, prompt, options):
        """Permite ao usuário selecionar uma opção"""
        print(f"\n{prompt}")
        for i, option in enumerate(options, 1):
            print(f"   {i}. {option}")
        
        while True:
            try:
                choice = int(input("Escolha (número): "))
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print("❌ Opção inválida. Tente novamente.")
            except ValueError:
                print("❌ Digite um número válido.")
    
    def configure_agent(self):
        """Configura um agente interativamente"""
        print("\n🤖 Configuração do Agente")
        print("=" * 40)
        
        # Configurações básicas
        self.config['nome'] = self.get_user_input("Nome do Agente", "Meu Assistente")
        self.config['papel'] = self.get_user_input("Papel/Função", "Assistente especializado")
        
        # Nível
        niveis = [
            "Nível 1: Ferramentas & Instruções",
            "Nível 2: Conhecimento & RAG",
            "Nível 3: Memória & Raciocínio",
            "Nível 4: Times de Agentes",
            "Nível 5: Workflows Agênticos"
        ]
        
        nivel_selecionado = self.select_option("Selecione o nível:", niveis)
        self.config['nivel'] = int(nivel_selecionado.split(':')[0].split()[1])
        
        # Provedor
        provedores = ["OpenAI", "Anthropic", "Google Gemini", "OpenRouter"]
        self.config['provedor'] = self.select_option("Selecione o provedor:", provedores)
        
        # Modelo
        modelos = self.get_model_options(self.config['provedor'])
        self.config['modelo'] = self.select_option("Selecione o modelo:", modelos)
        
        # Instruções
        print(f"\nInstruções do Agente:")
        print("(Digite as instruções. Linha vazia para finalizar)")
        instrucoes = []
        while True:
            linha = input(">>> ")
            if not linha:
                break
            instrucoes.append(linha)
        
        self.config['instrucoes'] = '\n'.join(instrucoes) if instrucoes else "Você é um assistente útil e especializado."
        
        # Ferramentas
        if self.config['nivel'] >= 1:
            ferramentas_disponiveis = [
                "DuckDuckGo (Busca)",
                "Calculator (Calculadora)",
                "YFinance (Dados Financeiros)",
                "Email (Email)",
                "Python (Código Python)"
            ]
            
            print(f"\nFerramentas disponíveis:")
            ferramentas_selecionadas = []
            
            for ferramenta in ferramentas_disponiveis:
                resposta = input(f"Incluir {ferramenta}? (y/N): ").lower()
                if resposta == 'y':
                    nome_ferramenta = ferramenta.split(' ')[0]
                    ferramentas_selecionadas.append(nome_ferramenta)
            
            self.config['ferramentas'] = ferramentas_selecionadas
        else:
            self.config['ferramentas'] = []
    
    def get_model_options(self, provedor):
        """Retorna opções de modelo por provedor"""
        modelos = {
            "OpenAI": ["gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4o"],
            "Anthropic": ["claude-3-5-sonnet", "claude-3-opus", "claude-3-haiku"],
            "Google Gemini": ["gemini-2.0-flash-001", "gemini-1.5-pro", "gemini-1.5-flash"],
            "OpenRouter": [
                "openai/gpt-4o", 
                "anthropic/claude-3-5-sonnet", 
                "meta-llama/llama-3.1-8b-instruct:free",
                "mistralai/mistral-7b-instruct:free"
            ]
        }
        return modelos.get(provedor, ["modelo-padrao"])
    
    def generate_code(self):
        """Gera código Python para o agente"""
        # Imports
        imports = ["from agno.agent import Agent"]
        
        if self.config['provedor'] == "OpenAI":
            imports.append("from agno.models.openai import OpenAIChat")
            model_class = "OpenAIChat"
        elif self.config['provedor'] == "Anthropic":
            imports.append("from agno.models.anthropic import Claude")
            model_class = "Claude"
        elif self.config['provedor'] == "Google Gemini":
            imports.append("from agno.models.google import Gemini")
            model_class = "Gemini"
        elif self.config['provedor'] == "OpenRouter":
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
        
        for ferramenta in self.config['ferramentas']:
            if ferramenta in tool_imports:
                imports.append(tool_imports[ferramenta])
        
        # Gerar código
        codigo = "\n".join(imports) + "\n\n"
        
        # Comentário sobre API
        api_comments = {
            "OpenAI": "# Configure: export OPENAI_API_KEY=sua_chave\n\n",
            "Anthropic": "# Configure: export ANTHROPIC_API_KEY=sua_chave\n\n",
            "Google Gemini": "# Configure: export GOOGLE_API_KEY=sua_chave\n\n",
            "OpenRouter": "# Configure: export OPENROUTER_API_KEY=sua_chave\n\n"
        }
        
        codigo += api_comments.get(self.config['provedor'], "")
        
        # Criar agente
        nome_var = self.config['nome'].lower().replace(' ', '_')
        codigo += f"""# Criar {self.config['nome']}
{nome_var} = Agent(
    name="{self.config['nome']}",
    role="{self.config['papel']}",
    model={model_class}(id="{self.config['modelo']}"),"""
        
        # Adicionar ferramentas
        if self.config['ferramentas']:
            codigo += "\n    tools=[\n"
            tool_classes = {
                "DuckDuckGo": "DuckDuckGoTools()",
                "Calculator": "CalculatorTools()",
                "YFinance": "YFinanceTools(stock_price=True)",
                "Email": "EmailTools()",
                "Python": "PythonTools()"
            }
            
            for ferramenta in self.config['ferramentas']:
                if ferramenta in tool_classes:
                    codigo += f"        {tool_classes[ferramenta]},\n"
            codigo += "    ],"
        
        # Instruções
        instrucoes_linhas = self.config['instrucoes'].split('\n')
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
    
    def save_code(self, codigo):
        """Salva o código gerado"""
        nome_arquivo = f"agente_{self.config['nome'].lower().replace(' ', '_')}.py"
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                f.write(codigo)
            print(f"✅ Código salvo em: {nome_arquivo}")
            return nome_arquivo
        except Exception as e:
            print(f"❌ Erro ao salvar código: {e}")
            return None
    
    def save_config(self):
        """Salva a configuração"""
        nome_arquivo = f"config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            print(f"✅ Configuração salva em: {nome_arquivo}")
            return nome_arquivo
        except Exception as e:
            print(f"❌ Erro ao salvar configuração: {e}")
            return None
    
    def show_summary(self):
        """Mostra resumo da configuração"""
        print(f"\n📋 Resumo da Configuração:")
        print(f"=" * 40)
        print(f"Nome: {self.config['nome']}")
        print(f"Papel: {self.config['papel']}")
        print(f"Nível: {self.config['nivel']}")
        print(f"Provedor: {self.config['provedor']}")
        print(f"Modelo: {self.config['modelo']}")
        print(f"Ferramentas: {', '.join(self.config['ferramentas']) if self.config['ferramentas'] else 'Nenhuma'}")
        print(f"Instruções: {self.config['instrucoes'][:50]}...")
    
    def run(self):
        """Executa a interface CLI"""
        print("🤖 Agno Agent Builder - CLI")
        print("=" * 50)
        
        # Verificações
        if not self.check_agno():
            return
        
        configured_apis = self.check_apis()
        if not configured_apis:
            print("\n⚠️ Nenhuma API configurada!")
            print("💡 Configure pelo menos uma API no arquivo .env")
            
            continuar = input("\nContinuar mesmo assim? (y/N): ").lower()
            if continuar != 'y':
                return
        
        # Configurar agente
        self.configure_agent()
        
        # Mostrar resumo
        self.show_summary()
        
        # Confirmar
        confirmar = input(f"\n✅ Configuração está correta? (Y/n): ").lower()
        if confirmar == 'n':
            print("❌ Configuração cancelada")
            return
        
        # Gerar código
        print(f"\n🔄 Gerando código...")
        codigo = self.generate_code()
        
        # Mostrar código
        print(f"\n📝 Código Gerado:")
        print("=" * 50)
        print(codigo)
        print("=" * 50)
        
        # Salvar arquivos
        salvar = input(f"\n💾 Salvar código e configuração? (Y/n): ").lower()
        if salvar != 'n':
            arquivo_codigo = self.save_code(codigo)
            arquivo_config = self.save_config()
            
            if arquivo_codigo:
                print(f"\n🚀 Para testar o agente:")
                print(f"   python {arquivo_codigo}")
        
        print(f"\n🎉 Agente criado com sucesso!")

def main():
    """Função principal"""
    try:
        builder = AgnoBuilderCLI()
        builder.run()
    except KeyboardInterrupt:
        print(f"\n\n👋 Operação cancelada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")

if __name__ == "__main__":
    main()