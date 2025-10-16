import requests
import logging
from typing import Dict, Optional
from django.conf import settings
from .models import AnalysisLog

logger = logging.getLogger('analysis')


class CNPJAService:
    """Serviço para consumir a API CNPJA"""
    
    def __init__(self):
        self.api_url = settings.CNPJA_API_URL
        self.api_token = settings.CNPJA_API_TOKEN
        self.headers = {
            'Accept': 'application/json',
            'Authorization': self.api_token
        }
    
    def _log_request(self, cnpj: str, level: str, message: str, details: Dict = None):
        """Log de requisições"""
        AnalysisLog.objects.create(
            cnpj=cnpj,
            level=level,
            message=message,
            details=details or {}
        )
        logger.log(
            getattr(logging, level),
            f"CNPJ {cnpj}: {message}",
            extra={'details': details}
        )
    
    def _clean_cnpj(self, cnpj: str) -> str:
        """Remove formatação do CNPJ"""
        return ''.join(filter(str.isdigit, cnpj))
    
    def _validate_cnpj(self, cnpj: str) -> bool:
        """Validação básica do CNPJ"""
        cnpj = self._clean_cnpj(cnpj)
        
        if len(cnpj) != 14:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cnpj == cnpj[0] * 14:
            return False
        
        return True
    
    def get_cnpj_data(self, cnpj: str) -> Optional[Dict]:
        """
        Busca dados do CNPJ na API CNPJA
        
        Args:
            cnpj: CNPJ para consulta
            
        Returns:
            Dict com dados do CNPJ ou None em caso de erro
        """
        cnpj_clean = self._clean_cnpj(cnpj)
        
        if not self._validate_cnpj(cnpj_clean):
            self._log_request(cnpj_clean, 'ERROR', 'CNPJ inválido')
            return None
        
        try:
            url = f"{self.api_url}/{cnpj_clean}"
            self._log_request(cnpj_clean, 'INFO', f'Fazendo requisição para {url}')
            
            response = requests.get(url, headers=self.headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                self._log_request(cnpj_clean, 'INFO', 'Dados obtidos com sucesso', {
                    'company_name': data.get('company', {}).get('name'),
                    'status': data.get('status', {}).get('text')
                })
                return data
            
            elif response.status_code == 404:
                self._log_request(cnpj_clean, 'WARNING', 'CNPJ não encontrado na API')
                return None
            
            elif response.status_code == 429:
                self._log_request(cnpj_clean, 'WARNING', 'Rate limit excedido')
                return None
            
            else:
                self._log_request(cnpj_clean, 'ERROR', f'Erro na API: {response.status_code}', {
                    'response_text': response.text[:500]
                })
                return None
                
        except requests.exceptions.Timeout:
            self._log_request(cnpj_clean, 'ERROR', 'Timeout na requisição')
            return None
            
        except requests.exceptions.ConnectionError:
            self._log_request(cnpj_clean, 'ERROR', 'Erro de conexão com a API')
            return None
            
        except Exception as e:
            self._log_request(cnpj_clean, 'ERROR', f'Erro inesperado: {str(e)}')
            return None
    
    def parse_cnpj_data(self, raw_data: Dict) -> Dict:
        """
        Extrai e organiza dados relevantes da resposta da API
        
        Args:
            raw_data: Dados brutos da API
            
        Returns:
            Dict com dados organizados
        """
        try:
            company = raw_data.get('company', {})
            address = raw_data.get('address', {})
            main_activity = raw_data.get('mainActivity', {})
            status = raw_data.get('status', {})
            
            parsed_data = {
                'cnpj': raw_data.get('taxId', ''),
                'company_name': company.get('name', ''),
                'status': status.get('text', ''),
                'founded_date': raw_data.get('founded', ''),
                'equity': company.get('equity'),
                'main_activity': main_activity.get('text', ''),
                'city': address.get('city', ''),
                'state': address.get('state', ''),
                'zip_code': address.get('zip', ''),
                'district': address.get('district', ''),
                'street': address.get('street', ''),
                'number': address.get('number', ''),
                'phones': raw_data.get('phones', []),
                'emails': raw_data.get('emails', []),
                'side_activities': raw_data.get('sideActivities', []),
                'members': company.get('members', []),
                'nature': company.get('nature', {}),
                'size': company.get('size', {}),
                'raw_data': raw_data
            }
            
            return parsed_data
            
        except Exception as e:
            logger.error(f"Erro ao processar dados do CNPJ: {str(e)}")
            return {}
