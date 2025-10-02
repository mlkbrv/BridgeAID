#!/usr/bin/env python
"""
Простой скрипт для тестирования настройки Django
"""

import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BridgeAID.settings')
django.setup()

try:
    from core.models import Employer, CandidateProfile, Vacancy
    from users.models import User
    
    print("✅ Импорт моделей успешен!")
    
    # Проверяем количество записей
    print(f"Пользователей: {User.objects.count()}")
    print(f"Работодателей: {Employer.objects.count()}")
    print(f"Кандидатов: {CandidateProfile.objects.count()}")
    print(f"Вакансий: {Vacancy.objects.count()}")
    
    print("✅ Все модели работают корректно!")
    
except Exception as e:
    print(f"❌ Ошибка: {e}")
    sys.exit(1)
