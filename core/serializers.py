from rest_framework import serializers
from decimal import Decimal
from django.core.validators import MinValueValidator
from .models import (
    Employer, CandidateProfile, Vacancy, Application, Document, 
    VisaCase, HousingListing, RelocationSuggestion, ExpenseEstimate, 
    AIAssistantInteraction
)
from users.models import User


class EmployerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    company_name = serializers.CharField(max_length=255)
    contact_email = serializers.EmailField()
    contact_phone = serializers.CharField(max_length=64, required=False, allow_blank=True, allow_null=True)
    country = serializers.CharField(max_length=64, default='CY')
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Employer
        fields = [
            'id', 'user', 'company_name', 'contact_email', 'contact_phone', 
            'country', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class CandidateProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    phone = serializers.CharField(max_length=64, required=False, allow_blank=True, allow_null=True)
    current_country = serializers.CharField(max_length=64, default='TR')
    resume = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    skills = serializers.JSONField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            'id', 'user', 'phone', 'current_country', 'resume', 
            'skills', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class VacancySerializer(serializers.ModelSerializer):
    employer = serializers.StringRelatedField(read_only=True)
    title = serializers.CharField(max_length=255)
    description = serializers.CharField()
    salary = serializers.DecimalField(max_digits=12, decimal_places=2, required=False, allow_null=True)
    currency = serializers.ChoiceField(choices=[
        ('EUR', 'Euro'),
        ('TRY', 'Turkish Lira'),
        ('USD', 'US Dollar'),
    ], default='EUR')
    location = serializers.CharField(max_length=255)
    remote = serializers.BooleanField(default=False)
    status = serializers.ChoiceField(choices=[
        ('open', 'Open'),
        ('closed', 'Closed'),
        ('paused', 'Paused'),
    ], default='open')
    created_at = serializers.DateTimeField(read_only=True)
    expires_at = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Vacancy
        fields = [
            'id', 'employer', 'title', 'description', 'salary', 'currency',
            'location', 'remote', 'status', 'created_at', 'expires_at'
        ]
        read_only_fields = ['id', 'created_at']


class ApplicationSerializer(serializers.ModelSerializer):
    vacancy = serializers.StringRelatedField(read_only=True)
    candidate = serializers.StringRelatedField(read_only=True)
    cover_letter = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    status = serializers.ChoiceField(choices=[
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='applied')
    submitted_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    score = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Application
        fields = [
            'id', 'vacancy', 'candidate', 'cover_letter', 'status',
            'submitted_at', 'updated_at', 'score'
        ]
        read_only_fields = ['id', 'submitted_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    owner = serializers.StringRelatedField(read_only=True)
    application = serializers.StringRelatedField(read_only=True)
    doc_type = serializers.ChoiceField(choices=[
        ('passport', 'Passport'),
        ('photo', 'Photo'),
        ('cv', 'CV'),
        ('contract', 'Contract'),
        ('visa_form', 'Visa Form'),
        ('other', 'Other'),
    ])
    file = serializers.FileField()
    metadata = serializers.JSONField(required=False, allow_null=True)
    uploaded_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id', 'owner', 'application', 'doc_type', 'file',
            'metadata', 'uploaded_at'
        ]
        read_only_fields = ['id', 'uploaded_at']


class VisaCaseSerializer(serializers.ModelSerializer):
    application = serializers.StringRelatedField(read_only=True)
    assigned_officer = serializers.StringRelatedField(read_only=True)
    status = serializers.CharField(max_length=64, default='initiated')
    steps = serializers.JSONField(default=list)
    instructions = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = VisaCase
        fields = [
            'id', 'application', 'assigned_officer', 'status', 'steps',
            'instructions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class HousingListingSerializer(serializers.ModelSerializer):
    provider_name = serializers.CharField(max_length=255, required=False, allow_blank=True, allow_null=True)
    address = serializers.CharField(max_length=512)
    city = serializers.CharField(max_length=128)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
    currency = serializers.ChoiceField(choices=[
        ('EUR', 'Euro'),
        ('TRY', 'Turkish Lira'),
        ('USD', 'US Dollar'),
    ], default='EUR')
    rooms = serializers.IntegerField(default=1)
    area_sqm = serializers.FloatField(required=False, allow_null=True)
    url = serializers.URLField(required=False, allow_blank=True, allow_null=True)
    distance_to_work_m = serializers.IntegerField(required=False, allow_null=True)
    commute_minutes = serializers.IntegerField(required=False, allow_null=True)
    listed_at = serializers.DateTimeField(read_only=True)
    metadata = serializers.JSONField(required=False, allow_null=True)

    class Meta:
        model = HousingListing
        fields = [
            'id', 'provider_name', 'address', 'city', 'price', 'currency',
            'rooms', 'area_sqm', 'url', 'distance_to_work_m', 'commute_minutes',
            'listed_at', 'metadata'
        ]
        read_only_fields = ['id', 'listed_at']


class RelocationSuggestionSerializer(serializers.ModelSerializer):
    application = serializers.StringRelatedField(read_only=True)
    housing = serializers.StringRelatedField(read_only=True)
    reason = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = RelocationSuggestion
        fields = [
            'id', 'application', 'housing', 'reason', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ExpenseEstimateSerializer(serializers.ModelSerializer):
    application = serializers.StringRelatedField(read_only=True)
    housing = serializers.StringRelatedField(read_only=True)
    daily_commute_cost = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    daily_food_cost = serializers.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    currency = serializers.ChoiceField(choices=[
        ('EUR', 'Euro'),
        ('TRY', 'Turkish Lira'),
        ('USD', 'US Dollar'),
    ], default='EUR')
    assumptions = serializers.JSONField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)
    daily_total = serializers.ReadOnlyField()

    class Meta:
        model = ExpenseEstimate
        fields = [
            'id', 'application', 'housing', 'daily_commute_cost', 'daily_food_cost',
            'currency', 'assumptions', 'created_at', 'daily_total'
        ]
        read_only_fields = ['id', 'created_at', 'daily_total']


class AIAssistantInteractionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    application = serializers.StringRelatedField(read_only=True)
    role = serializers.ChoiceField(choices=[('assistant', 'assistant'), ('user', 'user')], default='assistant')
    message = serializers.CharField()
    metadata = serializers.JSONField(required=False, allow_null=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = AIAssistantInteraction
        fields = [
            'id', 'user', 'application', 'role', 'message',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
