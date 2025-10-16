#!/usr/bin/env python
"""
Script de teste para o Sistema de Análise de CNPJ
Demonstra o funcionamento do sistema através de exemplos práticos
"""

import os
import sys
import django
from datetime import datetime

# Configuração do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cnpj_analyzer.settings')
django.setup()

from analysis.engines import CNPJAnalysisEngine
from analysis.models import CNPJData, AnalysisResult


def test_cnpj_analysis():
    """Testa a análise de CNPJ com exemplos"""
    
    print("=" * 60)
    print("SISTEMA DE ANÁLISE DE CNPJ - TESTE PRÁTICO")
    print("=" * 60)
    print()
    
    # CNPJs de teste (exemplos reais)
    test_cnpjs = [
        "37335118000180",  # CNPJA Tecnologia (do exemplo)
        "11222333000181",  # CNPJ de exemplo
        "12345678000195",  # CNPJ de exemplo
    ]
    
    engine = CNPJAnalysisEngine()
    
    for i, cnpj in enumerate(test_cnpjs, 1):
        print(f"TESTE {i}: Analisando CNPJ {cnpj}")
        print("-" * 40)
        
        try:
            # Executa análise
            result = engine.analyze_cnpj(cnpj)
            
            if result['success']:
                print(f"Analise concluida com sucesso!")
                print(f"Score: {result['overall_score']}")
                print(f"Status: {result['status']}")
                print(f"Risco: {result['risk_level']}")
                print(f"Tempo: {result['processing_time']:.2f}s")
                print()
                
                # Mostra critérios
                print("Criterios de Analise:")
                for criteria in result['criteria']:
                    status_icon = "OK" if criteria['passed'] else "ERRO"
                    print(f"  {status_icon} {criteria['name']}: {criteria['score']} pontos")
                    print(f"     {criteria['description']}")
                print()
                
            else:
                print(f"Erro na analise: {result['error']}")
                print()
                
        except Exception as e:
            print(f"Erro inesperado: {str(e)}")
            print()
    
    # Estatísticas gerais
    print("=" * 60)
    print("ESTATÍSTICAS DO SISTEMA")
    print("=" * 60)
    
    total_cnpjs = CNPJData.objects.count()
    total_analyses = AnalysisResult.objects.count()
    
    print(f"Total de CNPJs analisados: {total_cnpjs}")
    print(f"Total de analises realizadas: {total_analyses}")
    
    if total_analyses > 0:
        approved = AnalysisResult.objects.filter(status='APROVADO').count()
        attention = AnalysisResult.objects.filter(status='ATENCAO').count()
        rejected = AnalysisResult.objects.filter(status='REPROVADO').count()
        
        print(f"Aprovados: {approved} ({approved/total_analyses*100:.1f}%)")
        print(f"Atencao: {attention} ({attention/total_analyses*100:.1f}%)")
        print(f"Reprovados: {rejected} ({rejected/total_analyses*100:.1f}%)")
    
    print()
    print("Teste concluido com sucesso!")


def test_api_integration():
    """Testa a integração com a API CNPJA"""
    
    print("=" * 60)
    print("TESTE DE INTEGRAÇÃO COM API CNPJA")
    print("=" * 60)
    print()
    
    from analysis.services import CNPJAService
    
    service = CNPJAService()
    
    # Testa CNPJ válido
    test_cnpj = "37335118000180"
    print(f"Testando busca de CNPJ: {test_cnpj}")
    
    raw_data = service.get_cnpj_data(test_cnpj)
    
    if raw_data:
        print("Dados obtidos da API com sucesso!")
        
        parsed_data = service.parse_cnpj_data(raw_data)
        print(f"Empresa: {parsed_data.get('company_name', 'N/A')}")
        print(f"Status: {parsed_data.get('status', 'N/A')}")
        print(f"Cidade: {parsed_data.get('city', 'N/A')}")
        print(f"Estado: {parsed_data.get('state', 'N/A')}")
        print(f"Capital: R$ {parsed_data.get('equity', 0):,.2f}")
        print()
    else:
        print("Falha ao obter dados da API")
        print()


def show_system_info():
    """Mostra informações do sistema"""
    
    print("=" * 60)
    print("INFORMAÇÕES DO SISTEMA")
    print("=" * 60)
    print()
    
    print("Python:", sys.version.split()[0])
    print("Django:", django.get_version())
    print("Data/Hora:", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print()
    
    # Verifica configurações
    from django.conf import settings
    
    print("Configuracoes:")
    print(f"  - Debug: {settings.DEBUG}")
    print(f"  - Banco: {settings.DATABASES['default']['ENGINE']}")
    print(f"  - API CNPJA: {settings.CNPJA_API_URL}")
    print()


if __name__ == "__main__":
    try:
        show_system_info()
        test_api_integration()
        test_cnpj_analysis()
        
    except KeyboardInterrupt:
        print("\n\nTeste interrompido pelo usuario")
    except Exception as e:
        print(f"\n\nErro durante o teste: {str(e)}")
        import traceback
        traceback.print_exc()
