from django.contrib import admin
from .models import (
    Employer, CandidateProfile, Vacancy, Application, Document,
    VisaCase, HousingListing, RelocationSuggestion, ExpenseEstimate,
    AIAssistantInteraction
)


@admin.register(Employer)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'contact_email', 'country', 'created_at']
    list_filter = ['country', 'created_at']
    search_fields = ['company_name', 'contact_email']
    readonly_fields = ['id', 'created_at']


@admin.register(CandidateProfile)
class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_country', 'created_at']
    list_filter = ['current_country', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'user__email']
    readonly_fields = ['id', 'created_at']


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'location', 'status', 'salary', 'currency', 'created_at']
    list_filter = ['status', 'currency', 'remote', 'created_at']
    search_fields = ['title', 'description', 'location', 'employer__company_name']
    readonly_fields = ['id', 'created_at']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'vacancy', 'status', 'submitted_at', 'score']
    list_filter = ['status', 'submitted_at']
    search_fields = ['candidate__user__first_name', 'candidate__user__last_name', 'vacancy__title']
    readonly_fields = ['id', 'submitted_at', 'updated_at']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'doc_type', 'application', 'uploaded_at']
    list_filter = ['doc_type', 'uploaded_at']
    search_fields = ['owner__first_name', 'owner__last_name', 'doc_type']
    readonly_fields = ['id', 'uploaded_at']


@admin.register(VisaCase)
class VisaCaseAdmin(admin.ModelAdmin):
    list_display = ['application', 'assigned_officer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['application__candidate__user__first_name', 'assigned_officer__first_name']
    readonly_fields = ['id', 'created_at', 'updated_at']


@admin.register(HousingListing)
class HousingListingAdmin(admin.ModelAdmin):
    list_display = ['address', 'city', 'price', 'currency', 'rooms', 'listed_at']
    list_filter = ['currency', 'rooms', 'listed_at']
    search_fields = ['address', 'city', 'provider_name']
    readonly_fields = ['id', 'listed_at']


@admin.register(RelocationSuggestion)
class RelocationSuggestionAdmin(admin.ModelAdmin):
    list_display = ['application', 'housing', 'created_at']
    list_filter = ['created_at']
    search_fields = ['application__candidate__user__first_name', 'housing__address']
    readonly_fields = ['id', 'created_at']


@admin.register(ExpenseEstimate)
class ExpenseEstimateAdmin(admin.ModelAdmin):
    list_display = ['application', 'housing', 'daily_total', 'currency', 'created_at']
    list_filter = ['currency', 'created_at']
    search_fields = ['application__candidate__user__first_name', 'housing__address']
    readonly_fields = ['id', 'created_at']


@admin.register(AIAssistantInteraction)
class AIAssistantInteractionAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'application', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__first_name', 'user__last_name', 'message']
    readonly_fields = ['id', 'created_at']