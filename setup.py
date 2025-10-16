#!/usr/bin/env python
"""
Script de inicialização do Sistema de Análise de CNPJ
Configura o ambiente e executa as migrações necessárias
"""

import os
import sys
import subprocess
import django
from pathlib import Path

def run_command(command, description):
    """Executa um comando e mostra o resultado"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Concluído!")
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} - Erro!")
        print(f"   Erro: {e.stderr.strip()}")
        return False

def check_python_version():
    """Verifica se a versão do Python é adequada"""
    print("🐍 Verificando versão do Python...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK!")
    return True

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    try:
        import django
        import requests
        print("✅ Dependências principais - OK!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("   Execute: pip install -r requirements.txt")
        return False

def setup_environment():
    """Configura o ambiente Django"""
    print("⚙️ Configurando ambiente Django...")
    
    # Configura variáveis de ambiente
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cnpj_analyzer.settings')
    
    try:
        django.setup()
        print("✅ Ambiente Django configurado!")
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar Django: {e}")
        return False

def create_directories():
    """Cria diretórios necessários"""
    print("📁 Criando diretórios necessários...")
    
    directories = ['logs', 'static', 'media']
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"   ✅ {directory}/")
    
    return True

def run_migrations():
    """Executa as migrações do banco"""
    print("🗄️ Executando migrações do banco...")
    
    commands = [
        ("python manage.py makemigrations", "Criando migrações"),
        ("python manage.py migrate", "Aplicando migrações"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    
    return True

def create_superuser():
    """Cria superusuário se não existir"""
    print("👤 Verificando superusuário...")
    
    try:
        from django.contrib.auth.models import User
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superusuário já existe!")
            return True
        else:
            print("ℹ️ Nenhum superusuário encontrado.")
            print("   Para criar um superusuário, execute:")
            print("   python manage.py createsuperuser")
            return True
    except Exception as e:
        print(f"❌ Erro ao verificar superusuário: {e}")
        return False

def test_system():
    """Testa se o sistema está funcionando"""
    print("🧪 Testando sistema...")
    
    try:
        from analysis.engines import CNPJAnalysisEngine
        from analysis.services import CNPJAService
        
        # Testa se as classes podem ser importadas
        engine = CNPJAnalysisEngine()
        service = CNPJAService()
        
        print("✅ Sistema funcionando corretamente!")
        return True
    except Exception as e:
        print(f"❌ Erro no teste do sistema: {e}")
        return False

def show_next_steps():
    """Mostra próximos passos"""
    print("\n" + "="*60)
    print("🎉 SISTEMA CONFIGURADO COM SUCESSO!")
    print("="*60)
    print()
    print("📋 Próximos passos:")
    print("1. Execute o servidor:")
    print("   python manage.py runserver")
    print()
    print("2. Acesse o sistema:")
    print("   http://127.0.0.1:8000/")
    print()
    print("3. Para administração:")
    print("   http://127.0.0.1:8000/admin/")
    print()
    print("4. Para testar o sistema:")
    print("   python test_system.py")
    print()
    print("📚 Documentação:")
    print("   - README.md: Instruções completas")
    print("   - ARQUITETURA.md: Documentação técnica")
    print()

def main():
    """Função principal"""
    print("🚀 INICIALIZANDO SISTEMA DE ANÁLISE DE CNPJ")
    print("="*60)
    print()
    
    steps = [
        ("Verificar Python", check_python_version),
        ("Verificar dependências", check_dependencies),
        ("Criar diretórios", create_directories),
        ("Configurar ambiente", setup_environment),
        ("Executar migrações", run_migrations),
        ("Verificar superusuário", create_superuser),
        ("Testar sistema", test_system),
    ]
    
    for step_name, step_function in steps:
        print(f"\n📌 {step_name}")
        print("-" * 40)
        
        if not step_function():
            print(f"\n❌ Falha na etapa: {step_name}")
            print("   Verifique os erros acima e tente novamente.")
            return False
    
    show_next_steps()
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Inicialização concluída com sucesso!")
        else:
            print("\n❌ Inicialização falhou!")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n⏹️ Inicialização interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
