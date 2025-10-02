import uuid
from django.db import models
from decimal import Decimal
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User

CURRENCY_CHOICES = [
    ('EUR', 'Euro'),
    ('TRY', 'Turkish Lira'),
    ('USD', 'US Dollar'),
]

VACANCY_STATUS = [
    ('open', 'Open'),
    ('closed', 'Closed'),
    ('paused', 'Paused'),
]

APPLICATION_STATUS = [
    ('applied', 'Applied'),
    ('screening', 'Screening'),
    ('interview', 'Interview'),
    ('offered', 'Offered'),
    ('accepted', 'Accepted'),
    ('rejected', 'Rejected'),
]

DOCUMENT_TYPES = [
    ('passport', 'Passport'),
    ('photo', 'Photo'),
    ('cv', 'CV'),
    ('contract', 'Contract'),
    ('visa_form', 'Visa Form'),
    ('other', 'Other'),
]


class Employer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=64, blank=True, null=True)
    country = models.CharField(max_length=64, default='CY')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company_name}"

class CandidateProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    phone = models.CharField(max_length=64, blank=True, null=True)
    current_country = models.CharField(max_length=64, default='TR')
    resume = models.TextField(blank=True, null=True)
    skills = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"


class Vacancy(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE, related_name='vacancies')
    title = models.CharField(max_length=255)
    description = models.TextField()
    salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    location = models.CharField(max_length=255)
    remote = models.BooleanField(default=False)
    status = models.CharField(max_length=16, choices=VACANCY_STATUS, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['status', 'created_at']),
        ]

    def __str__(self):
        return f"{self.title} — {self.employer.company_name}"


class Application(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=16, choices=APPLICATION_STATUS, default='applied')
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    score = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('vacancy', 'candidate')

    def __str__(self):
        return f"{self.candidate} -> {self.vacancy} ({self.status})"


class Document(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='documents')
    doc_type = models.CharField(max_length=32, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='documents/%Y/%m/%d/')
    metadata = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.owner} - {self.doc_type}"


class VisaCase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.OneToOneField(Application, on_delete=models.CASCADE, related_name='visa_case')
    assigned_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_cases')
    status = models.CharField(max_length=64, default='initiated')
    steps = models.JSONField(default=list, blank=True)
    instructions = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def add_step(self, step: dict):
        s = self.steps or []
        s.append(step)
        self.steps = s
        self.save(update_fields=['steps', 'updated_at'])

    def __str__(self):
        return f"VisaCase for {self.application}"


class HousingListing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=512)
    city = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal('0.0'))])
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    rooms = models.IntegerField(default=1)
    area_sqm = models.FloatField(null=True, blank=True)
    url = models.URLField(blank=True, null=True)
    distance_to_work_m = models.IntegerField(null=True, blank=True)
    commute_minutes = models.IntegerField(null=True, blank=True)
    listed_at = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"{self.address} — {self.price} {self.currency}"


class RelocationSuggestion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='housing_suggestions')
    housing = models.ForeignKey(HousingListing, on_delete=models.CASCADE)
    reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('application', 'housing')

    def __str__(self):
        return f"Suggestion for {self.application} -> {self.housing}"


class ExpenseEstimate(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='expense_estimates')
    housing = models.ForeignKey(HousingListing, on_delete=models.SET_NULL, null=True, blank=True)
    daily_commute_cost = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    daily_food_cost = models.DecimalField(max_digits=8, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='EUR')
    assumptions = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def daily_total(self):
        return (self.daily_commute_cost or Decimal('0.00')) + (self.daily_food_cost or Decimal('0.00'))

    def __str__(self):
        return f"ExpenseEstimate {self.application} = {self.daily_total} {self.currency}"


class AIAssistantInteraction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_interactions')
    application = models.ForeignKey(Application, on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_interactions')
    role = models.CharField(max_length=32, choices=[('assistant','assistant'), ('user','user')], default='assistant')
    message = models.TextField()
    metadata = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AI msg to {self.user} at {self.created_at}"