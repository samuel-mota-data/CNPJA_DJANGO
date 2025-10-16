# 🏢 Sistema de Análise de CNPJ - Django

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

Sistema automatizado e inteligente para análise e avaliação de CNPJs, desenvolvido especificamente para avaliação de risco em crédito educacional. O sistema reduz o tempo de análise manual de 30 minutos para segundos, padronizando decisões através de critérios objetivos.

## 🎯 Visão Geral

Este projeto implementa uma solução completa de análise de CNPJs que:

- **Automatiza** o processo de avaliação de empresas
- **Padroniza** decisões através de critérios objetivos
- **Reduz** tempo de análise de 30 minutos para segundos
- **Integra** com APIs externas para dados atualizados
- **Fornece** interface web moderna e API REST completa

## ✨ Funcionalidades Principais

### 🔍 Análise Inteligente
- **6 critérios de avaliação** implementados
- **Sistema de pontuação ponderado** para decisões objetivas
- **Classificação automática** (Aprovado/Atenção/Reprovado)
- **Análise em tempo real** com dados atualizados

### 🌐 Interface Moderna
- **Design responsivo** com Bootstrap 5
- **Interface intuitiva** para análise de CNPJs
- **Visualização de resultados** em tempo real
- **Histórico completo** de análises realizadas

### 🔌 API REST Completa
- **Endpoints RESTful** para integração
- **Documentação automática** dos endpoints
- **Autenticação** e controle de acesso
- **Health checks** para monitoramento

### 📊 Critérios de Análise

| Critério | Peso | Descrição |
|----------|------|-----------|
| **Status Ativo** | 25% | Verifica se empresa está ativa |
| **Tempo de Operação** | 20% | Analisa estabilidade temporal |
| **Capital Social** | 20% | Avalia recursos financeiros |
| **Atividade Educação** | 15% | Verifica relação com educação |
| **Estrutura Societária** | 10% | Analisa administradores |
| **Localização** | 10% | Avalia posicionamento geográfico |

## 🛠️ Stack Tecnológico

### Backend
- **Django 4.2.7** - Framework web robusto
- **Python 3.8+** - Linguagem principal
- **SQLite/PostgreSQL** - Banco de dados
- **Requests** - Cliente HTTP para APIs

### Frontend
- **HTML5/CSS3** - Estrutura e estilização
- **Bootstrap 5** - Framework CSS responsivo
- **JavaScript** - Interatividade e AJAX
- **Font Awesome** - Ícones

### Integração
- **CNPJA API** - Dados de CNPJs atualizados
- **REST API** - Arquitetura de comunicação
- **JSON** - Formato de dados

## 🚀 Instalação Rápida

### 1. Clone o Repositório
```bash
git clone https://github.com/samuel-mota-data/CNPJA_DJANGO.git
cd CNPJA_DJANGO
```

### 2. Configure o Ambiente
```bash
# Crie ambiente virtual
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt
```

### 3. Configure Variáveis
```bash
# Copie arquivo de exemplo
cp .env.example .env

# Edite com suas configurações
# CNPJA_API_TOKEN=seu-token-aqui
```

### 4. Execute o Sistema
```bash
# Execute migrações
python manage.py migrate

# Inicie o servidor
python manage.py runserver

# Acesse: http://127.0.0.1:8000/
```

## 📖 Como Usar

### Interface Web
1. Acesse `http://127.0.0.1:8000/`
2. Digite o CNPJ (apenas números)
3. Clique em "Analisar CNPJ"
4. Visualize resultados detalhados

### API REST

#### Análise de CNPJ
```bash
curl -X POST http://127.0.0.1:8000/api/analyze/ \
  -H "Content-Type: application/json" \
  -d '{"cnpj": "37335118000180"}'
```

**Resposta:**
```json
{
  "success": true,
  "data": {
    "cnpj": "37335118000180",
    "company_name": "CNPJA TECNOLOGIA LTDA",
    "overall_score": 74,
    "status": "ATENCAO",
    "risk_level": "Médio",
    "processing_time": 1.67,
    "criteria": [...]
  }
}
```

#### Outros Endpoints
```bash
# Histórico de análises
GET /api/history/

# Detalhes de análise específica
GET /api/analysis/{id}/

# Busca de CNPJs
GET /api/search/?q=termo

# Health check
GET /api/health/
```

## 🧪 Testes

### Script de Teste Automático
```bash
python test_system.py
```

### Teste da API
```bash
python test_api.py
```

### Testes Unitários
```bash
python manage.py test
```

## 📊 Exemplo de Análise

**CNPJ Testado:** 37335118000180 (CNPJA Tecnologia)

**Resultado:**
- **Score:** 74 pontos
- **Status:** ATENÇÃO
- **Risco:** Médio
- **Tempo:** 1.67 segundos

**Critérios:**
- ✅ Status Ativo: 100 pontos
- ✅ Tempo Operação: 100 pontos (5.4 anos)
- ❌ Capital Social: 20 pontos (R$ 1.000)
- ⚠️ Atividade Educação: 50 pontos
- ✅ Estrutura Societária: 80 pontos
- ✅ Localização: 100 pontos (São Paulo/SP)

## 🗂️ Estrutura do Projeto

```
CNPJA_DJANGO/
├── 📁 cnpj_analyzer/          # Configurações Django
│   ├── settings.py           # Configurações principais
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # WSGI config
├── 📁 analysis/              # App principal
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views e endpoints
│   ├── engines.py           # Engine de análise
│   ├── services.py          # Serviço API CNPJA
│   ├── admin.py             # Interface administrativa
│   └── urls.py              # URLs do app
├── 📁 templates/             # Templates HTML
│   └── analysis/
│       └── index.html       # Interface principal
├── 📁 static/               # Arquivos estáticos
├── 📁 logs/                 # Logs do sistema
├── 📄 manage.py             # Script Django
├── 📄 requirements.txt      # Dependências
├── 📄 setup.py              # Script de configuração
├── 📄 test_system.py        # Testes do sistema
├── 📄 test_api.py           # Testes da API
├── 📄 README.md             # Este arquivo
├── 📄 ARQUITETURA.md        # Documentação técnica
└── 🗄️ db.sqlite3           # Banco de dados
```

## 🔧 Configuração Avançada

### Variáveis de Ambiente
```env
# Django
SECRET_KEY=sua-chave-secreta
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# API CNPJA
CNPJA_API_TOKEN=seu-token-da-api
CNPJA_API_URL=https://api.cnpja.com/office

# Banco de Dados (Produção)
DATABASE_URL=postgresql://user:pass@localhost:5432/cnpj_analyzer

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/django.log
```

### Produção
```bash
# Instalar PostgreSQL
pip install psycopg2-binary

# Configurar banco
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic

# Executar com Gunicorn
gunicorn cnpj_analyzer.wsgi:application
```

## 📈 Monitoramento

### Logs Estruturados
- **Arquivo:** `logs/django.log`
- **Console:** Durante desenvolvimento
- **Banco:** Tabela `analysis_analysislog`

### Métricas Importantes
- Volume de análises por dia
- Tempo médio de processamento
- Taxa de sucesso das análises
- Erros na API externa

### Health Check
```bash
curl http://127.0.0.1:8000/api/health/
```

## 🚨 Tratamento de Erros

O sistema trata automaticamente:
- ✅ CNPJs inválidos ou malformados
- ✅ CNPJs não encontrados na API
- ✅ Timeouts na API externa
- ✅ Erros de conexão
- ✅ Dados incompletos da API

## 🔄 Roadmap

### ✅ Implementado
- Sistema básico funcional
- Interface web responsiva
- API REST completa
- 6 critérios de análise
- Sistema de logs

### 🔄 Próximas Versões
- Cache de resultados
- Análise em lote
- Relatórios em PDF
- Dashboard de métricas
- Integração com APIs adicionais

</div>