from django.contrib import admin
from .models import CNPJData, AnalysisResult, AnalysisCriteria, AnalysisLog


@admin.register(CNPJData)
class CNPJDataAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'company_name', 'status', 'founded_date', 'equity', 'city', 'state']
    list_filter = ['status', 'state', 'founded_date']
    search_fields = ['cnpj', 'company_name']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['cnpj_data', 'overall_score', 'status', 'risk_level', 'analysis_date']
    list_filter = ['status', 'risk_level', 'analysis_date']
    search_fields = ['cnpj_data__cnpj', 'cnpj_data__company_name']
    readonly_fields = ['analysis_date']


@admin.register(AnalysisCriteria)
class AnalysisCriteriaAdmin(admin.ModelAdmin):
    list_display = ['analysis_result', 'criteria_name', 'score', 'weight', 'passed']
    list_filter = ['criteria_name', 'passed']
    search_fields = ['analysis_result__cnpj_data__cnpj']


@admin.register(AnalysisLog)
class AnalysisLogAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'level', 'message', 'timestamp']
    list_filter = ['level', 'timestamp']
    search_fields = ['cnpj', 'message']
    readonly_fields = ['timestamp']
