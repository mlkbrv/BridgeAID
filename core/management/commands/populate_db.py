from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import (
    Employer, CandidateProfile, Vacancy, Application, Document,
    VisaCase, HousingListing, RelocationSuggestion, ExpenseEstimate,
    AIAssistantInteraction
)
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Populates the database with test data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new ones',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            AIAssistantInteraction.objects.all().delete()
            ExpenseEstimate.objects.all().delete()
            RelocationSuggestion.objects.all().delete()
            HousingListing.objects.all().delete()
            VisaCase.objects.all().delete()
            Document.objects.all().delete()
            Application.objects.all().delete()
            Vacancy.objects.all().delete()
            CandidateProfile.objects.all().delete()
            Employer.objects.all().delete()
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write(self.style.SUCCESS('Data cleared'))

        self.stdout.write('Creating test data...')
        
        # Creating users
        users_data = [
            {
                'email': 'employer1@example.com',
                'first_name': 'John',
                'last_name': 'Smith',
                'phone': '+1234567890',
                'is_staff': False,
            },
            {
                'email': 'employer2@example.com',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'phone': '+1234567891',
                'is_staff': False,
            },
            {
                'email': 'candidate1@example.com',
                'first_name': 'Ahmed',
                'last_name': 'Hassan',
                'phone': '+905551234567',
                'is_staff': False,
            },
            {
                'email': 'candidate2@example.com',
                'first_name': 'Maria',
                'last_name': 'Garcia',
                'phone': '+905551234568',
                'is_staff': False,
            },
            {
                'email': 'candidate3@example.com',
                'first_name': 'Omar',
                'last_name': 'Al-Rashid',
                'phone': '+905551234569',
                'is_staff': False,
            },
            {
                'email': 'officer1@example.com',
                'first_name': 'David',
                'last_name': 'Wilson',
                'phone': '+1234567892',
                'is_staff': True,
            },
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults=user_data
            )
            if created:
                user.set_password('testpass123')
                user.save()
            users.append(user)
            self.stdout.write(f'Created user: {user.email}')
        
        # Creating employers
        employers_data = [
            {
                'user': users[0],
                'company_name': 'Tech Solutions Ltd',
                'contact_email': 'hr@techsolutions.com',
                'contact_phone': '+1234567890',
                'country': 'CY',
            },
            {
                'user': users[1],
                'company_name': 'Global Services Inc',
                'contact_email': 'careers@globalservices.com',
                'contact_phone': '+1234567891',
                'country': 'CY',
            },
        ]
        
        employers = []
        for emp_data in employers_data:
            employer, created = Employer.objects.get_or_create(
                user=emp_data['user'],
                defaults=emp_data
            )
            employers.append(employer)
            self.stdout.write(f'Created employer: {employer.company_name}')
        
        # Creating candidate profiles
        candidates_data = [
            {
                'user': users[2],
                'phone': '+905551234567',
                'current_country': 'TR',
                'resume': 'Experienced developer with 5+ years of experience in Python and Django',
                'skills': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
            },
            {
                'user': users[3],
                'phone': '+905551234568',
                'current_country': 'TR',
                'resume': 'Frontend developer with experience in React and Vue.js',
                'skills': ['JavaScript', 'React', 'Vue.js', 'CSS', 'HTML'],
            },
            {
                'user': users[4],
                'phone': '+905551234569',
                'current_country': 'TR',
                'resume': 'Full-stack developer with experience in web development',
                'skills': ['Python', 'JavaScript', 'Node.js', 'MongoDB', 'AWS'],
            },
        ]
        
        candidates = []
        for cand_data in candidates_data:
            candidate, created = CandidateProfile.objects.get_or_create(
                user=cand_data['user'],
                defaults=cand_data
            )
            candidates.append(candidate)
            self.stdout.write(f'Created candidate: {candidate.user.get_full_name()}')
        
        # Creating vacancies
        vacancies_data = [
            {
                'employer': employers[0],
                'title': 'Senior Python Developer',
                'description': 'Looking for an experienced Python developer to work on high-load systems',
                'salary': Decimal('5000.00'),
                'currency': 'EUR',
                'location': 'Nicosia, Cyprus',
                'remote': True,
                'status': 'open',
                'expires_at': timezone.now() + timedelta(days=30),
            },
            {
                'employer': employers[0],
                'title': 'Frontend Developer',
                'description': 'Need a Frontend developer to create modern web interfaces',
                'salary': Decimal('4000.00'),
                'currency': 'EUR',
                'location': 'Limassol, Cyprus',
                'remote': False,
                'status': 'open',
                'expires_at': timezone.now() + timedelta(days=45),
            },
            {
                'employer': employers[1],
                'title': 'Full Stack Developer',
                'description': 'Full cycle of web application development using modern technologies',
                'salary': Decimal('4500.00'),
                'currency': 'EUR',
                'location': 'Paphos, Cyprus',
                'remote': True,
                'status': 'open',
                'expires_at': timezone.now() + timedelta(days=60),
            },
        ]
        
        vacancies = []
        for vac_data in vacancies_data:
            vacancy, created = Vacancy.objects.get_or_create(
                title=vac_data['title'],
                employer=vac_data['employer'],
                defaults=vac_data
            )
            vacancies.append(vacancy)
            self.stdout.write(f'Created vacancy: {vacancy.title}')
        
        # Creating applications
        applications_data = [
            {
                'vacancy': vacancies[0],
                'candidate': candidates[0],
                'cover_letter': 'Interested in the Senior Python Developer position. I have experience with Django and PostgreSQL.',
                'status': 'applied',
                'score': 85.5,
            },
            {
                'vacancy': vacancies[0],
                'candidate': candidates[2],
                'cover_letter': 'Would like to participate in the project. Experience with Python and web development.',
                'status': 'screening',
                'score': 78.0,
            },
            {
                'vacancy': vacancies[1],
                'candidate': candidates[1],
                'cover_letter': 'Great opportunity for development in Frontend development.',
                'status': 'interview',
                'score': 92.0,
            },
            {
                'vacancy': vacancies[2],
                'candidate': candidates[2],
                'cover_letter': 'Interested in Full Stack development. Ready to relocate.',
                'status': 'applied',
                'score': 88.5,
            },
        ]
        
        applications = []
        for app_data in applications_data:
            application, created = Application.objects.get_or_create(
                vacancy=app_data['vacancy'],
                candidate=app_data['candidate'],
                defaults=app_data
            )
            applications.append(application)
            self.stdout.write(f'Created application: {application.candidate.user.get_full_name()} -> {application.vacancy.title}')
        
        # Creating documents
        documents_data = [
            {
                'owner': candidates[0].user,
                'application': applications[0],
                'doc_type': 'cv',
                'metadata': {'file_size': '2.5MB', 'pages': 3},
            },
            {
                'owner': candidates[0].user,
                'application': applications[0],
                'doc_type': 'passport',
                'metadata': {'file_size': '1.2MB', 'pages': 1},
            },
            {
                'owner': candidates[1].user,
                'application': applications[2],
                'doc_type': 'cv',
                'metadata': {'file_size': '1.8MB', 'pages': 2},
            },
        ]
        
        for doc_data in documents_data:
            document, created = Document.objects.get_or_create(
                owner=doc_data['owner'],
                application=doc_data['application'],
                doc_type=doc_data['doc_type'],
                defaults=doc_data
            )
            self.stdout.write(f'Created document: {document.doc_type} for {document.owner.get_full_name()}')
        
        # Creating visa cases
        visa_cases_data = [
            {
                'application': applications[0],
                'assigned_officer': users[5],
                'status': 'initiated',
                'steps': [
                    {'step': 'document_review', 'status': 'completed', 'date': timezone.now().isoformat()},
                    {'step': 'background_check', 'status': 'in_progress', 'date': timezone.now().isoformat()},
                ],
                'instructions': 'Check documents and conduct background check',
            },
            {
                'application': applications[2],
                'assigned_officer': users[5],
                'status': 'processing',
                'steps': [
                    {'step': 'document_review', 'status': 'completed', 'date': timezone.now().isoformat()},
                    {'step': 'interview_scheduled', 'status': 'completed', 'date': timezone.now().isoformat()},
                ],
                'instructions': 'Schedule interview with candidate',
            },
        ]
        
        for visa_data in visa_cases_data:
            visa_case, created = VisaCase.objects.get_or_create(
                application=visa_data['application'],
                defaults=visa_data
            )
            self.stdout.write(f'Created visa case for application: {visa_case.application.id}')
        
        # Creating housing listings
        housing_data = [
            {
                'provider_name': 'Cyprus Housing Ltd',
                'address': '123 Main Street, Nicosia',
                'city': 'Nicosia',
                'price': Decimal('1200.00'),
                'currency': 'EUR',
                'rooms': 2,
                'area_sqm': 75.5,
                'url': 'https://example.com/housing1',
                'distance_to_work_m': 1500,
                'commute_minutes': 20,
                'metadata': {'furnished': True, 'parking': True},
            },
            {
                'provider_name': 'Limassol Properties',
                'address': '456 Ocean View, Limassol',
                'city': 'Limassol',
                'price': Decimal('1500.00'),
                'currency': 'EUR',
                'rooms': 3,
                'area_sqm': 95.0,
                'url': 'https://example.com/housing2',
                'distance_to_work_m': 800,
                'commute_minutes': 15,
                'metadata': {'furnished': False, 'parking': True, 'balcony': True},
            },
            {
                'provider_name': 'Paphos Rentals',
                'address': '789 Hill Street, Paphos',
                'city': 'Paphos',
                'price': Decimal('900.00'),
                'currency': 'EUR',
                'rooms': 1,
                'area_sqm': 45.0,
                'url': 'https://example.com/housing3',
                'distance_to_work_m': 2000,
                'commute_minutes': 25,
                'metadata': {'furnished': True, 'parking': False},
            },
        ]
        
        housing_listings = []
        for house_data in housing_data:
            housing, created = HousingListing.objects.get_or_create(
                address=house_data['address'],
                defaults=house_data
            )
            housing_listings.append(housing)
            self.stdout.write(f'Created housing listing: {housing.address}')
        
        # Creating relocation suggestions
        relocation_suggestions_data = [
            {
                'application': applications[0],
                'housing': housing_listings[0],
                'reason': 'Close to office, good transport accessibility',
            },
            {
                'application': applications[2],
                'housing': housing_listings[1],
                'reason': 'Modern apartment with sea view, close to work',
            },
        ]
        
        for rel_data in relocation_suggestions_data:
            suggestion, created = RelocationSuggestion.objects.get_or_create(
                application=rel_data['application'],
                housing=rel_data['housing'],
                defaults=rel_data
            )
            self.stdout.write(f'Created relocation suggestion for application: {suggestion.application.id}')
        
        # Creating expense estimates
        expense_estimates_data = [
            {
                'application': applications[0],
                'housing': housing_listings[0],
                'daily_commute_cost': Decimal('5.00'),
                'daily_food_cost': Decimal('25.00'),
                'currency': 'EUR',
                'assumptions': {'transport_type': 'bus', 'meals_per_day': 3},
            },
            {
                'application': applications[2],
                'housing': housing_listings[1],
                'daily_commute_cost': Decimal('3.00'),
                'daily_food_cost': Decimal('30.00'),
                'currency': 'EUR',
                'assumptions': {'transport_type': 'walking', 'meals_per_day': 3},
            },
        ]
        
        for exp_data in expense_estimates_data:
            expense, created = ExpenseEstimate.objects.get_or_create(
                application=exp_data['application'],
                defaults=exp_data
            )
            self.stdout.write(f'Created expense estimate for application: {expense.application.id}')
        
        # Creating AI interactions
        ai_interactions_data = [
            {
                'user': candidates[0].user,
                'application': applications[0],
                'role': 'user',
                'message': 'What documents are needed to submit an application?',
                'metadata': {'session_id': 'session_001'},
            },
            {
                'user': candidates[0].user,
                'application': applications[0],
                'role': 'assistant',
                'message': 'To submit an application you will need: CV, passport, education diploma and criminal record certificate.',
                'metadata': {'session_id': 'session_001'},
            },
            {
                'user': candidates[1].user,
                'application': applications[2],
                'role': 'user',
                'message': 'When will the interview be?',
                'metadata': {'session_id': 'session_002'},
            },
            {
                'user': candidates[1].user,
                'application': applications[2],
                'role': 'assistant',
                'message': 'The interview is scheduled for next week. You will receive an invitation with details.',
                'metadata': {'session_id': 'session_002'},
            },
        ]
        
        for ai_data in ai_interactions_data:
            interaction, created = AIAssistantInteraction.objects.get_or_create(
                user=ai_data['user'],
                application=ai_data['application'],
                message=ai_data['message'],
                defaults=ai_data
            )
            self.stdout.write(f'Created AI interaction: {interaction.role} - {interaction.user.get_full_name()}')
        
        self.stdout.write(
            self.style.SUCCESS(
                f'\n✅ Test data successfully created!\n'
                f'Created:\n'
                f'- Users: {User.objects.count()}\n'
                f'- Employers: {Employer.objects.count()}\n'
                f'- Candidates: {CandidateProfile.objects.count()}\n'
                f'- Vacancies: {Vacancy.objects.count()}\n'
                f'- Applications: {Application.objects.count()}\n'
                f'- Documents: {Document.objects.count()}\n'
                f'- Visa Cases: {VisaCase.objects.count()}\n'
                f'- Housing Listings: {HousingListing.objects.count()}\n'
                f'- Relocation Suggestions: {RelocationSuggestion.objects.count()}\n'
                f'- Expense Estimates: {ExpenseEstimate.objects.count()}\n'
                f'- AI Interactions: {AIAssistantInteraction.objects.count()}'
            )
        )
