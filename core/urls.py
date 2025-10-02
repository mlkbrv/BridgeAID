from django.urls import path, include
from . import views

urlpatterns = [
    path('employers/', views.EmployerListCreateAPIView.as_view(), name='employer-list-create'),
    path('employers/<uuid:pk>/', views.EmployerRetrieveUpdateDestroyAPIView.as_view(), name='employer-detail'),
    
    path('candidates/', views.CandidateProfileListCreateAPIView.as_view(), name='candidate-list-create'),
    path('candidates/<uuid:pk>/', views.CandidateProfileRetrieveUpdateDestroyAPIView.as_view(), name='candidate-detail'),
    
    path('vacancies/', views.VacancyListCreateAPIView.as_view(), name='vacancy-list-create'),
    path('vacancies/<uuid:pk>/', views.VacancyRetrieveUpdateDestroyAPIView.as_view(), name='vacancy-detail'),
    path('employers/vacancies/', views.VacancyListByEmployerAPIView.as_view(), name='employer-vacancies'),
    
    path('applications/', views.ApplicationListCreateAPIView.as_view(), name='application-list-create'),
    path('applications/<uuid:pk>/', views.ApplicationRetrieveUpdateDestroyAPIView.as_view(), name='application-detail'),
    path('candidates/applications/', views.ApplicationListByCandidateAPIView.as_view(), name='candidate-applications'),
    path('vacancies/<uuid:vacancy_id>/applications/', views.ApplicationListByVacancyAPIView.as_view(), name='vacancy-applications'),
    
    path('documents/', views.DocumentListCreateAPIView.as_view(), name='document-list-create'),
    path('documents/<uuid:pk>/', views.DocumentRetrieveUpdateDestroyAPIView.as_view(), name='document-detail'),
    path('users/documents/', views.DocumentListByUserAPIView.as_view(), name='user-documents'),
    path('applications/<uuid:application_id>/documents/', views.DocumentListByApplicationAPIView.as_view(), name='application-documents'),
    
    path('visa-cases/', views.VisaCaseListCreateAPIView.as_view(), name='visa-case-list-create'),
    path('visa-cases/<uuid:pk>/', views.VisaCaseRetrieveUpdateDestroyAPIView.as_view(), name='visa-case-detail'),
    path('officers/visa-cases/', views.VisaCaseListByOfficerAPIView.as_view(), name='officer-visa-cases'),
    
    path('housing/', views.HousingListingListCreateAPIView.as_view(), name='housing-list-create'),
    path('housing/<uuid:pk>/', views.HousingListingRetrieveUpdateDestroyAPIView.as_view(), name='housing-detail'),
    
    path('relocation-suggestions/', views.RelocationSuggestionListCreateAPIView.as_view(), name='relocation-suggestion-list-create'),
    path('relocation-suggestions/<uuid:pk>/', views.RelocationSuggestionRetrieveUpdateDestroyAPIView.as_view(), name='relocation-suggestion-detail'),
    path('applications/<uuid:application_id>/relocation-suggestions/', views.RelocationSuggestionListByApplicationAPIView.as_view(), name='application-relocation-suggestions'),
    
    path('expense-estimates/', views.ExpenseEstimateListCreateAPIView.as_view(), name='expense-estimate-list-create'),
    path('expense-estimates/<uuid:pk>/', views.ExpenseEstimateRetrieveUpdateDestroyAPIView.as_view(), name='expense-estimate-detail'),
    path('applications/<uuid:application_id>/expense-estimates/', views.ExpenseEstimateListByApplicationAPIView.as_view(), name='application-expense-estimates'),
    
    path('ai-interactions/', views.AIAssistantInteractionListCreateAPIView.as_view(), name='ai-interaction-list-create'),
    path('ai-interactions/<uuid:pk>/', views.AIAssistantInteractionRetrieveUpdateDestroyAPIView.as_view(), name='ai-interaction-detail'),
    path('users/ai-interactions/', views.AIAssistantInteractionListByUserAPIView.as_view(), name='user-ai-interactions'),
    path('applications/<uuid:application_id>/ai-interactions/', views.AIAssistantInteractionListByApplicationAPIView.as_view(), name='application-ai-interactions'),
    
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
]
