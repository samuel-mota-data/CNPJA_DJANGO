import logging
from datetime import datetime, date
from typing import Dict, List, Tuple
from decimal import Decimal
from .models import CNPJData, AnalysisResult, AnalysisCriteria
from .services import CNPJAService

logger = logging.getLogger('analysis')


class CNPJAnalysisEngine:
    """Engine principal para análise de CNPJs"""
    
    def __init__(self):
        self.cnpja_service = CNPJAService()
        self.criteria_weights = {
            'status_ativo': 0.25,
            'tempo_operacao': 0.20,
            'capital_social': 0.20,
            'atividade_educacao': 0.15,
            'estrutura_societaria': 0.10,
            'localizacao': 0.10
        }
    
    def analyze_cnpj(self, cnpj: str) -> Dict:
        """
        Executa análise completa do CNPJ
        
        Args:
            cnpj: CNPJ para análise
            
        Returns:
            Dict com resultado da análise
        """
        start_time = datetime.now()
        
        try:
            # Busca dados na API
            raw_data = self.cnpja_service.get_cnpj_data(cnpj)
            if not raw_data:
                return {
                    'success': False,
                    'error': 'CNPJ não encontrado ou dados indisponíveis'
                }
            
            # Processa dados
            parsed_data = self.cnpja_service.parse_cnpj_data(raw_data)
            
            # Salva dados básicos
            cnpj_data = self._save_cnpj_data(parsed_data)
            
            # Executa análise
            analysis_results = self._execute_analysis(parsed_data)
            
            # Calcula score final
            overall_score = self._calculate_overall_score(analysis_results)
            status = self._determine_status(overall_score)
            risk_level = self._determine_risk_level(overall_score)
            
            # Salva resultado
            processing_time = (datetime.now() - start_time).total_seconds()
            analysis_result = self._save_analysis_result(
                cnpj_data, overall_score, status, risk_level, processing_time
            )
            
            # Salva critérios
            self._save_analysis_criteria(analysis_result, analysis_results)
            
            return {
                'success': True,
                'cnpj_data': cnpj_data,
                'analysis_result': analysis_result,
                'criteria': analysis_results,
                'overall_score': overall_score,
                'status': status,
                'risk_level': risk_level,
                'processing_time': processing_time
            }
            
        except Exception as e:
            logger.error(f"Erro na análise do CNPJ {cnpj}: {str(e)}")
            return {
                'success': False,
                'error': f'Erro interno: {str(e)}'
            }
    
    def _save_cnpj_data(self, parsed_data: Dict) -> CNPJData:
        """Salva dados básicos do CNPJ"""
        cnpj_clean = parsed_data['cnpj']
        
        # Converte data de fundação
        founded_date = None
        if parsed_data['founded_date']:
            try:
                founded_date = datetime.strptime(parsed_data['founded_date'], '%Y-%m-%d').date()
            except:
                pass
        
        cnpj_data, created = CNPJData.objects.get_or_create(
            cnpj=cnpj_clean,
            defaults={
                'company_name': parsed_data['company_name'],
                'status': parsed_data['status'],
                'founded_date': founded_date,
                'equity': parsed_data['equity'],
                'main_activity': parsed_data['main_activity'],
                'city': parsed_data['city'],
                'state': parsed_data['state']
            }
        )
        
        if not created:
            # Atualiza dados existentes
            cnpj_data.company_name = parsed_data['company_name']
            cnpj_data.status = parsed_data['status']
            cnpj_data.founded_date = founded_date
            cnpj_data.equity = parsed_data['equity']
            cnpj_data.main_activity = parsed_data['main_activity']
            cnpj_data.city = parsed_data['city']
            cnpj_data.state = parsed_data['state']
            cnpj_data.save()
        
        return cnpj_data
    
    def _execute_analysis(self, parsed_data: Dict) -> List[Dict]:
        """Executa todos os critérios de análise"""
        criteria_results = []
        
        # Critério 1: Status Ativo
        criteria_results.append(self._analyze_status_ativo(parsed_data))
        
        # Critério 2: Tempo de Operação
        criteria_results.append(self._analyze_tempo_operacao(parsed_data))
        
        # Critério 3: Capital Social
        criteria_results.append(self._analyze_capital_social(parsed_data))
        
        # Critério 4: Atividade de Educação
        criteria_results.append(self._analyze_atividade_educacao(parsed_data))
        
        # Critério 5: Estrutura Societária
        criteria_results.append(self._analyze_estrutura_societaria(parsed_data))
        
        # Critério 6: Localização
        criteria_results.append(self._analyze_localizacao(parsed_data))
        
        return criteria_results
    
    def _analyze_status_ativo(self, data: Dict) -> Dict:
        """Analisa se a empresa está ativa"""
        status = data.get('status', '').lower()
        
        if 'ativa' in status:
            score = 100
            passed = True
            description = "Empresa com status ativo"
        elif 'suspensa' in status:
            score = 30
            passed = False
            description = "Empresa suspensa - requer atenção"
        elif 'baixada' in status or 'inativa' in status:
            score = 0
            passed = False
            description = "Empresa inativa ou baixada"
        else:
            score = 50
            passed = False
            description = f"Status desconhecido: {status}"
        
        return {
            'name': 'status_ativo',
            'description': description,
            'score': score,
            'weight': self.criteria_weights['status_ativo'],
            'passed': passed,
            'details': {'status': data.get('status', '')}
        }
    
    def _analyze_tempo_operacao(self, data: Dict) -> Dict:
        """Analisa tempo de operação da empresa"""
        founded_date = data.get('founded_date')
        
        if not founded_date:
            return {
                'name': 'tempo_operacao',
                'description': 'Data de fundação não disponível',
                'score': 0,
                'weight': self.criteria_weights['tempo_operacao'],
                'passed': False,
                'details': {}
            }
        
        try:
            founded = datetime.strptime(founded_date, '%Y-%m-%d').date()
            today = date.today()
            years_operating = (today - founded).days / 365.25
            
            if years_operating >= 5:
                score = 100
                passed = True
                description = f"Empresa operando há {years_operating:.1f} anos - excelente estabilidade"
            elif years_operating >= 2:
                score = 80
                passed = True
                description = f"Empresa operando há {years_operating:.1f} anos - boa estabilidade"
            elif years_operating >= 1:
                score = 60
                passed = False
                description = f"Empresa operando há {years_operating:.1f} anos - requer atenção"
            else:
                score = 20
                passed = False
                description = f"Empresa muito nova ({years_operating:.1f} anos) - alto risco"
            
            return {
                'name': 'tempo_operacao',
                'description': description,
                'score': score,
                'weight': self.criteria_weights['tempo_operacao'],
                'passed': passed,
                'details': {
                    'founded_date': founded_date,
                    'years_operating': round(years_operating, 1)
                }
            }
            
        except Exception as e:
            return {
                'name': 'tempo_operacao',
                'description': f'Erro ao processar data de fundação: {str(e)}',
                'score': 0,
                'weight': self.criteria_weights['tempo_operacao'],
                'passed': False,
                'details': {'error': str(e)}
            }
    
    def _analyze_capital_social(self, data: Dict) -> Dict:
        """Analisa capital social da empresa"""
        equity = data.get('equity')
        
        if not equity:
            return {
                'name': 'capital_social',
                'description': 'Capital social não informado',
                'score': 30,
                'weight': self.criteria_weights['capital_social'],
                'passed': False,
                'details': {}
            }
        
        equity_decimal = Decimal(str(equity))
        
        if equity_decimal >= Decimal('1000000'):  # >= R$ 1M
            score = 100
            passed = True
            description = f"Capital social robusto: R$ {equity_decimal:,.2f}"
        elif equity_decimal >= Decimal('100000'):  # >= R$ 100k
            score = 80
            passed = True
            description = f"Capital social adequado: R$ {equity_decimal:,.2f}"
        elif equity_decimal >= Decimal('50000'):  # >= R$ 50k
            score = 60
            passed = False
            description = f"Capital social baixo: R$ {equity_decimal:,.2f}"
        else:
            score = 20
            passed = False
            description = f"Capital social muito baixo: R$ {equity_decimal:,.2f}"
        
        return {
            'name': 'capital_social',
            'description': description,
            'score': score,
            'weight': self.criteria_weights['capital_social'],
            'passed': passed,
            'details': {'equity': float(equity_decimal)}
        }
    
    def _analyze_atividade_educacao(self, data: Dict) -> Dict:
        """Analisa se a atividade principal é relacionada à educação"""
        main_activity = data.get('main_activity', '').lower()
        side_activities = [act.get('text', '').lower() for act in data.get('side_activities', [])]
        
        education_keywords = [
            'educação', 'educacao', 'ensino', 'escola', 'universidade', 'faculdade',
            'curso', 'treinamento', 'capacitação', 'formação', 'pedagógico',
            'acadêmico', 'escolar', 'educacional', 'didático', 'instrução'
        ]
        
        # Verifica atividade principal
        main_score = 0
        if any(keyword in main_activity for keyword in education_keywords):
            main_score = 100
        
        # Verifica atividades secundárias
        side_score = 0
        education_side_activities = 0
        for activity in side_activities:
            if any(keyword in activity for keyword in education_keywords):
                education_side_activities += 1
        
        if education_side_activities > 0:
            side_score = min(50, education_side_activities * 10)
        
        total_score = max(main_score, side_score)
        
        if total_score >= 80:
            passed = True
            description = "Atividade principal relacionada à educação"
        elif total_score >= 50:
            passed = False
            description = "Algumas atividades relacionadas à educação"
        else:
            passed = False
            description = "Atividades não relacionadas à educação"
        
        return {
            'name': 'atividade_educacao',
            'description': description,
            'score': total_score,
            'weight': self.criteria_weights['atividade_educacao'],
            'passed': passed,
            'details': {
                'main_activity': data.get('main_activity', ''),
                'education_side_activities': education_side_activities,
                'total_side_activities': len(side_activities)
            }
        }
    
    def _analyze_estrutura_societaria(self, data: Dict) -> Dict:
        """Analisa estrutura societária da empresa"""
        members = data.get('members', [])
        
        if not members:
            return {
                'name': 'estrutura_societaria',
                'description': 'Informações societárias não disponíveis',
                'score': 50,
                'weight': self.criteria_weights['estrutura_societaria'],
                'passed': False,
                'details': {}
            }
        
        # Conta sócios administradores
        administrators = [m for m in members if 'administrador' in m.get('role', {}).get('text', '').lower()]
        
        if len(administrators) >= 2:
            score = 100
            passed = True
            description = f"Boa estrutura societária com {len(administrators)} administradores"
        elif len(administrators) == 1:
            score = 80
            passed = True
            description = "Estrutura societária adequada com 1 administrador"
        else:
            score = 40
            passed = False
            description = "Estrutura societária pode ser melhorada"
        
        return {
            'name': 'estrutura_societaria',
            'description': description,
            'score': score,
            'weight': self.criteria_weights['estrutura_societaria'],
            'passed': passed,
            'details': {
                'total_members': len(members),
                'administrators': len(administrators),
                'members_info': [
                    {
                        'name': m.get('person', {}).get('name', ''),
                        'role': m.get('role', {}).get('text', ''),
                        'since': m.get('since', '')
                    }
                    for m in members
                ]
            }
        }
    
    def _analyze_localizacao(self, data: Dict) -> Dict:
        """Analisa localização da empresa"""
        state = data.get('state', '').upper()
        city = data.get('city', '').lower()
        
        # Estados com maior concentração de IES
        major_states = ['SP', 'RJ', 'MG', 'RS', 'PR', 'SC', 'BA', 'GO', 'DF']
        
        # Cidades com maior concentração de IES
        major_cities = [
            'são paulo', 'rio de janeiro', 'belo horizonte', 'porto alegre',
            'curitiba', 'florianópolis', 'salvador', 'goiânia', 'brasília',
            'fortaleza', 'recife', 'manaus', 'belém', 'campinas', 'santos'
        ]
        
        score = 50  # Score base
        
        if state in major_states:
            score += 30
        
        if any(major_city in city for major_city in major_cities):
            score += 20
        
        if score >= 80:
            passed = True
            description = f"Localização estratégica: {city.title()}/{state}"
        elif score >= 60:
            passed = True
            description = f"Localização adequada: {city.title()}/{state}"
        else:
            passed = False
            description = f"Localização pode ser melhorada: {city.title()}/{state}"
        
        return {
            'name': 'localizacao',
            'description': description,
            'score': score,
            'weight': self.criteria_weights['localizacao'],
            'passed': passed,
            'details': {
                'state': state,
                'city': city.title(),
                'is_major_state': state in major_states,
                'is_major_city': any(major_city in city for major_city in major_cities)
            }
        }
    
    def _calculate_overall_score(self, criteria_results: List[Dict]) -> int:
        """Calcula score geral ponderado"""
        total_weighted_score = 0
        total_weight = 0
        
        for criteria in criteria_results:
            weight = criteria['weight']
            score = criteria['score']
            
            total_weighted_score += score * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0
        
        return round(total_weighted_score / total_weight)
    
    def _determine_status(self, score: int) -> str:
        """Determina status baseado no score"""
        if score >= 80:
            return 'APROVADO'
        elif score >= 60:
            return 'ATENCAO'
        else:
            return 'REPROVADO'
    
    def _determine_risk_level(self, score: int) -> str:
        """Determina nível de risco baseado no score"""
        if score >= 80:
            return 'Baixo'
        elif score >= 60:
            return 'Médio'
        else:
            return 'Alto'
    
    def _save_analysis_result(self, cnpj_data: CNPJData, overall_score: int, 
                            status: str, risk_level: str, processing_time: float) -> AnalysisResult:
        """Salva resultado da análise"""
        analysis_result, created = AnalysisResult.objects.get_or_create(
            cnpj_data=cnpj_data,
            defaults={
                'overall_score': overall_score,
                'status': status,
                'risk_level': risk_level,
                'processing_time': processing_time
            }
        )
        
        if not created:
            analysis_result.overall_score = overall_score
            analysis_result.status = status
            analysis_result.risk_level = risk_level
            analysis_result.processing_time = processing_time
            analysis_result.save()
        
        return analysis_result
    
    def _save_analysis_criteria(self, analysis_result: AnalysisResult, criteria_results: List[Dict]):
        """Salva critérios da análise"""
        # Remove critérios antigos
        AnalysisCriteria.objects.filter(analysis_result=analysis_result).delete()
        
        # Salva novos critérios
        for criteria in criteria_results:
            AnalysisCriteria.objects.create(
                analysis_result=analysis_result,
                criteria_name=criteria['name'],
                criteria_description=criteria['description'],
                score=criteria['score'],
                weight=criteria['weight'],
                passed=criteria['passed'],
                details=criteria['details']
            )
