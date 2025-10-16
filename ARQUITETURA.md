# ARQUITETURA DO SISTEMA DE ANÁLISE DE CNPJ

## 1. VISÃO GERAL DA SOLUÇÃO

O Sistema de Análise de CNPJ é uma solução automatizada desenvolvida para avaliar empresas através de múltiplos critérios, reduzindo o tempo de análise manual de 30 minutos para segundos e padronizando as decisões de crédito educacional.

### Principais Componentes:
- **Frontend Web**: Interface responsiva para análise de CNPJs
- **API REST**: Endpoints para integração com outros sistemas
- **Engine de Análise**: Sistema inteligente de avaliação multi-critério
- **Serviço de Integração**: Consumo da API CNPJA
- **Sistema de Logs**: Rastreabilidade completa das decisões
- **Banco de Dados**: Armazenamento de dados e histórico

### Comunicação entre Componentes:
```
Frontend ↔ API REST ↔ Engine de Análise ↔ Serviço CNPJA ↔ API Externa
                ↓
        Banco de Dados + Sistema de Logs
```

## 2. ARQUITETURA DE COMPONENTES

### Componente Principal: CNPJAnalysisEngine
**Responsabilidade**: Orquestrar todo o processo de análise
- Coordena busca de dados na API externa
- Executa todos os critérios de análise
- Calcula score final ponderado
- Determina status e nível de risco
- Persiste resultados no banco

### Componente de Serviço: CNPJAService
**Responsabilidade**: Integração com API externa
- Validação de CNPJ
- Consumo da API CNPJA
- Tratamento de erros e timeouts
- Parsing e normalização de dados
- Logging de requisições

### Fluxo de Informação:
1. **Entrada**: CNPJ via interface web ou API
2. **Validação**: Verificação de formato e dígitos
3. **Busca**: Consulta à API CNPJA
4. **Análise**: Execução de 6 critérios paralelos
5. **Cálculo**: Score ponderado e classificação
6. **Persistência**: Salva dados e resultados
7. **Retorno**: Resultado estruturado para o usuário

## 3. ESTRATÉGIA DE ANÁLISE

### Dados Analisados:
- **Cadastrais**: Nome, status, data de fundação
- **Financeiros**: Capital social, estrutura societária
- **Operacionais**: Atividades principais e secundárias
- **Geográficos**: Localização (cidade/estado)
- **Societários**: Membros e administradores

### Critérios de Classificação:

#### 1. Status Ativo (25% do peso)
- **Aprovado**: Empresa ativa
- **Atenção**: Empresa suspensa
- **Reprovado**: Empresa inativa/baixada

#### 2. Tempo de Operação (20% do peso)
- **Excelente**: >5 anos (100 pontos)
- **Bom**: 2-5 anos (80 pontos)
- **Atenção**: 1-2 anos (60 pontos)
- **Risco**: <1 ano (20 pontos)

#### 3. Capital Social (20% do peso)
- **Robusto**: >R$ 1M (100 pontos)
- **Adequado**: R$ 100k-1M (80 pontos)
- **Baixo**: R$ 50k-100k (60 pontos)
- **Muito Baixo**: <R$ 50k (20 pontos)

#### 4. Atividade de Educação (15% do peso)
- **Relacionada**: Atividade principal/secundária em educação (100 pontos)
- **Parcial**: Algumas atividades relacionadas (50 pontos)
- **Não Relacionada**: Sem atividades educacionais (0 pontos)

#### 5. Estrutura Societária (10% do peso)
- **Boa**: 2+ administradores (100 pontos)
- **Adequada**: 1 administrador (80 pontos)
- **Melhorável**: Estrutura insuficiente (40 pontos)

#### 6. Localização (10% do peso)
- **Estratégica**: Estados/cidades com alta concentração de IES (100 pontos)
- **Adequada**: Localização razoável (80 pontos)
- **Melhorável**: Localização pode ser melhorada (50 pontos)

### Decisão Final:
- **APROVADO** (80-100 pontos): Baixo risco, adequado para crédito
- **ATENÇÃO** (60-79 pontos): Médio risco, requer análise adicional
- **REPROVADO** (0-59 pontos): Alto risco, não recomendado

### Formato da Saída:
```json
{
  "success": true,
  "data": {
    "cnpj": "37335118000180",
    "company_name": "CNPJA TECNOLOGIA LTDA",
    "overall_score": 85,
    "status": "APROVADO",
    "risk_level": "Baixo",
    "processing_time": 2.34,
    "criteria": [
      {
        "name": "status_ativo",
        "description": "Empresa com status ativo",
        "score": 100,
        "weight": 0.25,
        "passed": true
      }
    ]
  }
}
```

## 4. STACK TECNOLÓGICO

### Backend:
- **Django 4.2.7**: Framework web robusto e escalável
- **Python 3.8+**: Linguagem principal
- **SQLite**: Banco de dados para desenvolvimento
- **PostgreSQL**: Recomendado para produção

### Frontend:
- **HTML5/CSS3**: Estrutura e estilização
- **Bootstrap 5**: Framework CSS responsivo
- **JavaScript**: Interatividade e AJAX
- **Font Awesome**: Ícones

### Integração:
- **Requests**: Cliente HTTP para API externa
- **JSON**: Formato de dados
- **REST API**: Arquitetura de comunicação

### Ferramentas de IA:
- **Não utilizadas**: Solução baseada em regras determinísticas
- **Justificativa**: Maior transparência, menor custo, resultados previsíveis

### Considerações de Custo:
- **API CNPJA**: Gratuita com rate limit
- **Hosting**: Baixo custo (Django + SQLite)
- **Manutenção**: Mínima (sistema determinístico)

## 5. ESTRATÉGIA DE IMPLEMENTAÇÃO

### MVP (Mínimo Viável):
✅ **Implementado**:
- Interface web funcional
- Integração com API CNPJA
- 6 critérios de análise
- Sistema de logs
- API REST completa
- Histórico de análises

### Roadmap de Evolução:

#### Fase 1 (Atual):
- ✅ Sistema básico funcional
- ✅ Interface web responsiva
- ✅ API REST completa

#### Fase 2 (Próximas 4 semanas):
- 🔄 Cache de resultados para otimização
- 🔄 Análise em lote (batch processing)
- 🔄 Relatórios em PDF
- 🔄 Dashboard com métricas

#### Fase 3 (Próximos 3 meses):
- 🔄 Integração com APIs adicionais (Receita Federal)
- 🔄 Machine Learning para refinamento de critérios
- 🔄 Notificações automáticas
- 🔄 API GraphQL

#### Fase 4 (Próximos 6 meses):
- 🔄 Sistema multi-tenant
- 🔄 Integração com sistemas de CRM
- 🔄 Análise preditiva de risco
- 🔄 Mobile app

### Principais Desafios Técnicos:
1. **Rate Limiting**: Implementar cache inteligente
2. **Escalabilidade**: Migrar para PostgreSQL + Redis
3. **Confiabilidade**: Implementar retry e circuit breaker
4. **Performance**: Otimizar consultas e implementar paginação

### Estratégia de Testes:
- **Testes Unitários**: Critérios de análise individuais
- **Testes de Integração**: API externa e banco de dados
- **Testes de Carga**: Performance com múltiplos CNPJs
- **Testes de Aceitação**: Fluxos completos de usuário

## 6. OBSERVABILIDADE E MONITORAMENTO

### Rastreabilidade das Decisões:
- **Logs Estruturados**: Cada análise gera log detalhado
- **Auditoria**: Histórico completo de todas as análises
- **Metadados**: Timestamp, tempo de processamento, versão do sistema

### Logs Importantes:
```python
# Exemplo de log estruturado
{
  "timestamp": "2025-01-16T10:30:00Z",
  "level": "INFO",
  "cnpj": "37335118000180",
  "action": "analysis_completed",
  "score": 85,
  "status": "APROVADO",
  "processing_time": 2.34,
  "criteria_scores": {
    "status_ativo": 100,
    "tempo_operacao": 80,
    "capital_social": 90
  }
}
```

### Métricas Importantes:
- **Volume**: CNPJs analisados por dia/hora
- **Performance**: Tempo médio de análise
- **Qualidade**: Taxa de sucesso das análises
- **Erros**: Falhas na API externa, CNPJs inválidos

### Identificação e Correção de Erros:
- **Alertas**: Notificações para falhas críticas
- **Dashboard**: Monitoramento em tempo real
- **Logs Centralizados**: Facilita debugging
- **Health Checks**: Verificação contínua do sistema

### Exemplo de Monitoramento:
```python
# Health check endpoint
GET /api/health/
{
  "status": "healthy",
  "api_cnpja": "operational",
  "database": "connected",
  "uptime": "99.9%",
  "last_analysis": "2025-01-16T10:30:00Z"
}
```

## CONCLUSÃO

Esta arquitetura oferece uma solução robusta, escalável e transparente para análise automatizada de CNPJs. O sistema reduz significativamente o tempo de análise manual enquanto mantém a qualidade e rastreabilidade das decisões, atendendo perfeitamente aos requisitos de uma fintech de crédito educacional.

A escolha por uma abordagem determinística (ao invés de IA/ML) garante transparência total nas decisões, facilita auditoria regulatória e reduz custos operacionais, sendo ideal para o contexto de crédito educacional onde explicabilidade é fundamental.
