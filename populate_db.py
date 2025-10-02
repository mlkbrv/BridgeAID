#!/usr/bin/env python
"""
Скрипт для популяции базы данных тестовыми данными
Запуск: python manage.py shell < populate_db.py
"""

import os
import sys
import django
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BridgeAID.settings')
django.setup()

from django.contrib.auth import get_user_model
from core.models import (
    Employer, CandidateProfile, Vacancy, Application, Document,
    VisaCase, HousingListing, RelocationSuggestion, ExpenseEstimate,
    AIAssistantInteraction
)

User = get_user_model()

def create_test_data():
    print("Создание тестовых данных...")
    
    # Создание пользователей
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
        print(f"Создан пользователь: {user.email}")
    
    # Создание работодателей
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
        print(f"Создан работодатель: {employer.company_name}")
    
    # Создание профилей кандидатов
    candidates_data = [
        {
            'user': users[2],
            'phone': '+905551234567',
            'current_country': 'TR',
            'resume': 'Опытный разработчик с 5+ лет опыта в Python и Django',
            'skills': ['Python', 'Django', 'React', 'PostgreSQL', 'Docker'],
        },
        {
            'user': users[3],
            'phone': '+905551234568',
            'current_country': 'TR',
            'resume': 'Frontend разработчик с опытом в React и Vue.js',
            'skills': ['JavaScript', 'React', 'Vue.js', 'CSS', 'HTML'],
        },
        {
            'user': users[4],
            'phone': '+905551234569',
            'current_country': 'TR',
            'resume': 'Full-stack разработчик с опытом в веб-разработке',
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
        print(f"Создан кандидат: {candidate.user.get_full_name()}")
    
    # Создание вакансий
    vacancies_data = [
        {
            'employer': employers[0],
            'title': 'Senior Python Developer',
            'description': 'Ищем опытного Python разработчика для работы над высоконагруженными системами',
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
            'description': 'Требуется Frontend разработчик для создания современных веб-интерфейсов',
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
            'description': 'Полный цикл разработки веб-приложений с использованием современных технологий',
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
        print(f"Создана вакансия: {vacancy.title}")
    
    # Создание заявок
    applications_data = [
        {
            'vacancy': vacancies[0],
            'candidate': candidates[0],
            'cover_letter': 'Заинтересован в позиции Senior Python Developer. Имею опыт работы с Django и PostgreSQL.',
            'status': 'applied',
            'score': 85.5,
        },
        {
            'vacancy': vacancies[0],
            'candidate': candidates[2],
            'cover_letter': 'Хотел бы принять участие в проекте. Опыт работы с Python и веб-разработкой.',
            'status': 'screening',
            'score': 78.0,
        },
        {
            'vacancy': vacancies[1],
            'candidate': candidates[1],
            'cover_letter': 'Отличная возможность для развития в Frontend разработке.',
            'status': 'interview',
            'score': 92.0,
        },
        {
            'vacancy': vacancies[2],
            'candidate': candidates[2],
            'cover_letter': 'Интересуюсь Full Stack разработкой. Готов к переезду.',
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
        print(f"Создана заявка: {application.candidate.user.get_full_name()} -> {application.vacancy.title}")
    
    # Создание документов
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
        print(f"Создан документ: {document.doc_type} для {document.owner.get_full_name()}")
    
    # Создание визовых дел
    visa_cases_data = [
        {
            'application': applications[0],
            'assigned_officer': users[5],
            'status': 'initiated',
            'steps': [
                {'step': 'document_review', 'status': 'completed', 'date': timezone.now().isoformat()},
                {'step': 'background_check', 'status': 'in_progress', 'date': timezone.now().isoformat()},
            ],
            'instructions': 'Проверить документы и провести проверку биографии',
        },
        {
            'application': applications[2],
            'assigned_officer': users[5],
            'status': 'processing',
            'steps': [
                {'step': 'document_review', 'status': 'completed', 'date': timezone.now().isoformat()},
                {'step': 'interview_scheduled', 'status': 'completed', 'date': timezone.now().isoformat()},
            ],
            'instructions': 'Запланировать интервью с кандидатом',
        },
    ]
    
    for visa_data in visa_cases_data:
        visa_case, created = VisaCase.objects.get_or_create(
            application=visa_data['application'],
            defaults=visa_data
        )
        print(f"Создано визовое дело для заявки: {visa_case.application.id}")
    
    # Создание предложений жилья
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
        print(f"Создано предложение жилья: {housing.address}")
    
    # Создание предложений по переезду
    relocation_suggestions_data = [
        {
            'application': applications[0],
            'housing': housing_listings[0],
            'reason': 'Близко к офису, хорошая транспортная доступность',
        },
        {
            'application': applications[2],
            'housing': housing_listings[1],
            'reason': 'Современная квартира с видом на море, рядом с работой',
        },
    ]
    
    for rel_data in relocation_suggestions_data:
        suggestion, created = RelocationSuggestion.objects.get_or_create(
            application=rel_data['application'],
            housing=rel_data['housing'],
            defaults=rel_data
        )
        print(f"Создано предложение по переезду для заявки: {suggestion.application.id}")
    
    # Создание оценок расходов
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
        print(f"Создана оценка расходов для заявки: {expense.application.id}")
    
    # Создание AI взаимодействий
    ai_interactions_data = [
        {
            'user': candidates[0].user,
            'application': applications[0],
            'role': 'user',
            'message': 'Какие документы нужны для подачи заявки?',
            'metadata': {'session_id': 'session_001'},
        },
        {
            'user': candidates[0].user,
            'application': applications[0],
            'role': 'assistant',
            'message': 'Для подачи заявки вам понадобятся: CV, паспорт, диплом об образовании и справка о несудимости.',
            'metadata': {'session_id': 'session_001'},
        },
        {
            'user': candidates[1].user,
            'application': applications[2],
            'role': 'user',
            'message': 'Когда будет интервью?',
            'metadata': {'session_id': 'session_002'},
        },
        {
            'user': candidates[1].user,
            'application': applications[2],
            'role': 'assistant',
            'message': 'Интервью запланировано на следующую неделю. Вам придет приглашение с деталями.',
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
        print(f"Создано AI взаимодействие: {interaction.role} - {interaction.user.get_full_name()}")
    
    print("\n✅ Тестовые данные успешно созданы!")
    print(f"Создано:")
    print(f"- Пользователей: {User.objects.count()}")
    print(f"- Работодателей: {Employer.objects.count()}")
    print(f"- Кандидатов: {CandidateProfile.objects.count()}")
    print(f"- Вакансий: {Vacancy.objects.count()}")
    print(f"- Заявок: {Application.objects.count()}")
    print(f"- Документов: {Document.objects.count()}")
    print(f"- Визовых дел: {VisaCase.objects.count()}")
    print(f"- Предложений жилья: {HousingListing.objects.count()}")
    print(f"- Предложений по переезду: {RelocationSuggestion.objects.count()}")
    print(f"- Оценок расходов: {ExpenseEstimate.objects.count()}")
    print(f"- AI взаимодействий: {AIAssistantInteraction.objects.count()}")

if __name__ == '__main__':
    create_test_data()
