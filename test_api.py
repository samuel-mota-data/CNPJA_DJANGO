#!/usr/bin/env python
"""
Script para testar a API do Sistema de Análise de CNPJ
"""

import requests
import json

def test_api():
    """Testa a API de análise"""
    
    print("Testando API de Análise de CNPJ")
    print("=" * 40)
    
    # URL da API
    url = "http://127.0.0.1:8000/api/analyze/"
    
    # Dados de teste
    test_data = {
        "cnpj": "37335118000180"
    }
    
    try:
        print(f"Enviando requisição para: {url}")
        print(f"Dados: {test_data}")
        
        # Faz a requisição
        response = requests.post(
            url,
            json=test_data,
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print("SUCESSO!")
            print(f"Resultado: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print("ERRO!")
            print(f"Resposta: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("ERRO de conexao - servidor nao esta rodando")
    except requests.exceptions.Timeout:
        print("ERRO - Timeout na requisicao")
    except Exception as e:
        print(f"ERRO inesperado: {str(e)}")

def test_health():
    """Testa o health check"""
    
    print("\nTestando Health Check")
    print("=" * 40)
    
    try:
        response = requests.get("http://127.0.0.1:8000/api/health/", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("SUCESSO - Health Check OK!")
            print(f"Status: {result}")
        else:
            print(f"ERRO - Health Check falhou: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO no health check: {str(e)}")

def test_history():
    """Testa o histórico"""
    
    print("\nTestando Histórico")
    print("=" * 40)
    
    try:
        response = requests.get("http://127.0.0.1:8000/api/history/", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print("SUCESSO - Historico OK!")
            print(f"Total de analises: {len(result.get('data', []))}")
        else:
            print(f"ERRO - Historico falhou: {response.status_code}")
            
    except Exception as e:
        print(f"ERRO no historico: {str(e)}")

if __name__ == "__main__":
    test_health()
    test_history()
    test_api()
