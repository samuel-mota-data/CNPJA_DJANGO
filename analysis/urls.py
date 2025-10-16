from django.urls import path
from . import views

urlpatterns = [
    path('', views.CNPJAnalysisView.as_view(), name='analysis_home'),
    path('api/analyze/', views.analyze_cnpj_api, name='analyze_api'),
    path('api/history/', views.AnalysisHistoryView.as_view(), name='analysis_history'),
    path('api/analysis/<int:analysis_id>/', views.AnalysisDetailView.as_view(), name='analysis_detail'),
    path('api/search/', views.CNPJSearchView.as_view(), name='cnpj_search'),
    path('api/health/', views.health_check, name='health_check'),
]
