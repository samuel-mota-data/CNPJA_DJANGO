from django.db import models
from django.utils import timezone


class CNPJData(models.Model):
    """Modelo para armazenar dados básicos do CNPJ"""
    
    cnpj = models.CharField(max_length=14, unique=True, db_index=True)
    company_name = models.CharField(max_length=255)
    status = models.CharField(max_length=50)
    founded_date = models.DateField()
    equity = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    main_activity = models.CharField(max_length=500)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Dados do CNPJ"
        verbose_name_plural = "Dados dos CNPJs"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.cnpj} - {self.company_name}"


class AnalysisResult(models.Model):
    """Modelo para armazenar resultados das análises"""
    
    STATUS_CHOICES = [
        ('APROVADO', 'Aprovado'),
        ('ATENCAO', 'Atenção'),
        ('REPROVADO', 'Reprovado'),
    ]
    
    cnpj_data = models.OneToOneField(CNPJData, on_delete=models.CASCADE, related_name='analysis')
    overall_score = models.IntegerField(help_text="Score de 0 a 100")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    risk_level = models.CharField(max_length=20, help_text="Baixo, Médio, Alto")
    analysis_date = models.DateTimeField(default=timezone.now)
    processing_time = models.FloatField(help_text="Tempo de processamento em segundos")
    
    class Meta:
        verbose_name = "Resultado da Análise"
        verbose_name_plural = "Resultados das Análises"
        ordering = ['-analysis_date']
    
    def __str__(self):
        return f"Análise {self.cnpj_data.cnpj} - {self.status}"


class AnalysisCriteria(models.Model):
    """Modelo para armazenar critérios individuais da análise"""
    
    analysis_result = models.ForeignKey(AnalysisResult, on_delete=models.CASCADE, related_name='criteria')
    criteria_name = models.CharField(max_length=100)
    criteria_description = models.TextField()
    score = models.IntegerField(help_text="Score de 0 a 100 para este critério")
    weight = models.FloatField(help_text="Peso do critério na análise geral")
    passed = models.BooleanField()
    details = models.JSONField(default=dict, help_text="Detalhes específicos do critério")
    
    class Meta:
        verbose_name = "Critério da Análise"
        verbose_name_plural = "Critérios das Análises"
        ordering = ['-weight']
    
    def __str__(self):
        return f"{self.criteria_name} - {self.analysis_result.cnpj_data.cnpj}"


class AnalysisLog(models.Model):
    """Modelo para logs de análise"""
    
    LOG_LEVEL_CHOICES = [
        ('INFO', 'Informação'),
        ('WARNING', 'Aviso'),
        ('ERROR', 'Erro'),
        ('DEBUG', 'Debug'),
    ]
    
    cnpj = models.CharField(max_length=14, db_index=True)
    level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
    message = models.TextField()
    details = models.JSONField(default=dict)
    timestamp = models.DateTimeField(default=timezone.now)
    
    class Meta:
        verbose_name = "Log de Análise"
        verbose_name_plural = "Logs de Análise"
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.level} - {self.cnpj} - {self.timestamp}"
