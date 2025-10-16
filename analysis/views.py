from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from django.db import models
import json
import logging

from .models import CNPJData, AnalysisResult, AnalysisCriteria
from .engines import CNPJAnalysisEngine

logger = logging.getLogger('analysis')


class CNPJAnalysisView(View):
    """View principal para análise de CNPJ"""
    
    def get(self, request):
        """Renderiza página principal"""
        return render(request, 'analysis/index.html')
    
    def post(self, request):
        """Processa análise de CNPJ"""
        try:
            data = json.loads(request.body)
            cnpj = data.get('cnpj', '').strip()
            
            if not cnpj:
                return JsonResponse({
                    'success': False,
                    'error': 'CNPJ é obrigatório'
                }, status=400)
            
            # Executa análise
            engine = CNPJAnalysisEngine()
            result = engine.analyze_cnpj(cnpj)
            
            if result['success']:
                return JsonResponse({
                    'success': True,
                    'data': {
                        'cnpj': result['cnpj_data'].cnpj,
                        'company_name': result['cnpj_data'].company_name,
                        'overall_score': result['overall_score'],
                        'status': result['status'],
                        'risk_level': result['risk_level'],
                        'processing_time': result['processing_time'],
                        'criteria': [
                            {
                                'name': c['name'],
                                'description': c['description'],
                                'score': c['score'],
                                'weight': c['weight'],
                                'passed': c['passed']
                            }
                            for c in result['criteria']
                        ]
                    }
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': result['error']
                }, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'JSON inválido'
            }, status=400)
        except Exception as e:
            logger.error(f"Erro na view de análise: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': 'Erro interno do servidor'
            }, status=500)


class AnalysisHistoryView(View):
    """View para histórico de análises"""
    
    def get(self, request):
        """Lista análises realizadas"""
        analyses = AnalysisResult.objects.select_related('cnpj_data').prefetch_related('criteria').order_by('-analysis_date')[:50]
        
        data = []
        for analysis in analyses:
            data.append({
                'id': analysis.id,
                'cnpj': analysis.cnpj_data.cnpj,
                'company_name': analysis.cnpj_data.company_name,
                'overall_score': analysis.overall_score,
                'status': analysis.status,
                'risk_level': analysis.risk_level,
                'analysis_date': analysis.analysis_date.isoformat(),
                'processing_time': analysis.processing_time
            })
        
        return JsonResponse({
            'success': True,
            'data': data
        })


class AnalysisDetailView(View):
    """View para detalhes de uma análise específica"""
    
    def get(self, request, analysis_id):
        """Retorna detalhes de uma análise"""
        analysis = get_object_or_404(
            AnalysisResult.objects.select_related('cnpj_data').prefetch_related('criteria'),
            id=analysis_id
        )
        
        criteria_data = []
        for criteria in analysis.criteria.all():
            criteria_data.append({
                'name': criteria.criteria_name,
                'description': criteria.criteria_description,
                'score': criteria.score,
                'weight': criteria.weight,
                'passed': criteria.passed,
                'details': criteria.details
            })
        
        return JsonResponse({
            'success': True,
            'data': {
                'analysis_id': analysis.id,
                'cnpj_data': {
                    'cnpj': analysis.cnpj_data.cnpj,
                    'company_name': analysis.cnpj_data.company_name,
                    'status': analysis.cnpj_data.status,
                    'founded_date': analysis.cnpj_data.founded_date.isoformat() if analysis.cnpj_data.founded_date else None,
                    'equity': float(analysis.cnpj_data.equity) if analysis.cnpj_data.equity else None,
                    'main_activity': analysis.cnpj_data.main_activity,
                    'city': analysis.cnpj_data.city,
                    'state': analysis.cnpj_data.state
                },
                'analysis_result': {
                    'overall_score': analysis.overall_score,
                    'status': analysis.status,
                    'risk_level': analysis.risk_level,
                    'analysis_date': analysis.analysis_date.isoformat(),
                    'processing_time': analysis.processing_time
                },
                'criteria': criteria_data
            }
        })


class CNPJSearchView(View):
    """View para busca de CNPJs"""
    
    def get(self, request):
        """Busca CNPJs por nome ou CNPJ"""
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse({
                'success': False,
                'error': 'Parâmetro de busca é obrigatório'
            }, status=400)
        
        # Busca por CNPJ ou nome da empresa
        from django.db.models import Q
        cnpjs = CNPJData.objects.filter(
            Q(cnpj__icontains=query) | 
            Q(company_name__icontains=query)
        )[:20]
        
        data = []
        for cnpj in cnpjs:
            data.append({
                'cnpj': cnpj.cnpj,
                'company_name': cnpj.company_name,
                'status': cnpj.status,
                'city': cnpj.city,
                'state': cnpj.state,
                'has_analysis': hasattr(cnpj, 'analysis')
            })
        
        return JsonResponse({
            'success': True,
            'data': data
        })


@csrf_exempt
@require_http_methods(["POST"])
def analyze_cnpj_api(request):
    """API endpoint para análise de CNPJ"""
    try:
        data = json.loads(request.body)
        cnpj = data.get('cnpj', '').strip()
        
        if not cnpj:
            return JsonResponse({
                'success': False,
                'error': 'CNPJ é obrigatório'
            }, status=400)
        
        engine = CNPJAnalysisEngine()
        result = engine.analyze_cnpj(cnpj)
        
        if result['success']:
            # Serializa os dados corretamente
            serialized_result = {
                'success': True,
                'data': {
                    'cnpj': result['cnpj_data'].cnpj,
                    'company_name': result['cnpj_data'].company_name,
                    'overall_score': result['overall_score'],
                    'status': result['status'],
                    'risk_level': result['risk_level'],
                    'processing_time': result['processing_time'],
                    'criteria': [
                        {
                            'name': c['name'],
                            'description': c['description'],
                            'score': c['score'],
                            'weight': c['weight'],
                            'passed': c['passed']
                        }
                        for c in result['criteria']
                    ]
                }
            }
            return JsonResponse(serialized_result)
        else:
            return JsonResponse(result)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'JSON inválido'
        }, status=400)
    except Exception as e:
        logger.error(f"Erro na API de análise: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Erro interno do servidor'
        }, status=500)


def health_check(request):
    """Endpoint de health check"""
    return JsonResponse({
        'status': 'healthy',
        'service': 'CNPJ Analysis API',
        'version': '1.0.0'
    })
