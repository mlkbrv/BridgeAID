# BridgeAID 🌉

A comprehensive job placement platform that bridges the gap between job seekers and employers, with integrated visa processing and relocation assistance.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Mobile App](#mobile-app)
- [Database Management](#database-management)
- [Docker Deployment](#docker-deployment)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Overview

BridgeAID is a full-stack platform designed to streamline the job placement process for international candidates. It combines job search functionality with visa processing assistance and relocation support, making it easier for candidates to find opportunities abroad and for employers to hire international talent.

### Key Components

- **Backend API**: Django REST Framework-based API
- **Mobile App**: React Native application with Expo
- **Database**: SQLite (development) / PostgreSQL (production)
- **Containerization**: Docker support for easy deployment

## ✨ Features

### 🔐 Authentication & User Management
- User registration and login
- JWT-based authentication
- Role-based access control (Candidates, Employers, Officers)
- Secure password handling

### 💼 Job Management
- Job posting and management for employers
- Advanced job search and filtering
- Application tracking system
- Real-time status updates

### 📋 Application Processing
- Application submission and tracking
- Document management system
- Cover letter and resume handling
- Application status workflow

### 📁 Document Management
- Secure document upload and storage
- Document type categorization
- File metadata tracking
- Document-application linking

### 🏠 Relocation Support
- Housing listing management
- Relocation suggestions
- Expense estimation tools
- Location-based recommendations

### 🤖 AI Assistant
- Intelligent job matching
- Application guidance
- Document verification assistance
- Automated responses

### 📱 Mobile Experience
- Native mobile app for iOS and Android
- Offline capability
- Push notifications
- Intuitive user interface

## 🛠 Technology Stack

### Backend
- **Framework**: Django 4.2+
- **API**: Django REST Framework
- **Database**: SQLite (dev) / PostgreSQL (prod)
- **Authentication**: JWT tokens
- **File Storage**: Local / AWS S3
- **Containerization**: Docker

### Frontend (Mobile)
- **Framework**: React Native
- **Platform**: Expo
- **Navigation**: React Navigation
- **UI Components**: React Native Paper
- **State Management**: React Context
- **HTTP Client**: Axios

### Development Tools
- **Version Control**: Git
- **Package Management**: npm, pip
- **Code Quality**: ESLint, Prettier
- **Testing**: Jest, Django TestCase

## 📁 Project Structure

```
BridgeAID/
├── BridgeAID/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                      # Core application
│   ├── models.py              # Database models
│   ├── views.py               # API views
│   ├── serializers.py         # Data serializers
│   ├── urls.py                # URL routing
│   └── management/
│       └── commands/
│           └── populate_db.py # Database seeding
├── users/                     # User management
│   ├── models.py              # User models
│   ├── views.py               # Auth views
│   └── serializers.py
├── frontend/                  # React Native app
│   ├── App.js                 # Main app component
│   ├── package.json           # Dependencies
│   ├── src/
│   │   ├── screens/           # App screens
│   │   ├── navigation/        # Navigation setup
│   │   ├── context/           # State management
│   │   ├── services/          # API services
│   │   └── theme/             # App theming
│   └── assets/                # App assets
├── tools/                     # Utility tools
├── fixtures/                  # Database fixtures
├── requirements.txt           # Python dependencies
├── docker-compose.yml         # Docker configuration
├── Dockerfile                 # Docker image
└── README.md                  # This file
```

## 📋 Prerequisites

Before running the application, ensure you have the following installed:

- **Python 3.8+**
- **Node.js 16+**
- **npm or yarn**
- **Git**
- **Docker** (optional, for containerized deployment)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd BridgeAID
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate database with test data
python manage.py populate_db
```

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# For iOS development (macOS only)
cd ios && pod install && cd ..
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# API Settings
API_BASE_URL=http://localhost:8000/api

# File Storage
MEDIA_ROOT=media/
STATIC_ROOT=static/

# Email Settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Mobile App Configuration

Update `frontend/src/services/api.js` with your API base URL:

```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

## 🏃‍♂️ Running the Application

### Backend (Django API)

```bash
# Start the Django development server
python manage.py runserver

# The API will be available at http://localhost:8000
# Admin panel at http://localhost:8000/admin
```

### Frontend (React Native)

```bash
cd frontend

# Start the Expo development server
npm start

# Run on specific platforms
npm run android    # Android
npm run ios        # iOS
npm run web        # Web browser
```

### Using Docker

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# Stop services
docker-compose down
```

## 📚 API Documentation

### Authentication Endpoints

- `POST /api/auth/login/` - User login
- `POST /api/auth/register/` - User registration
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

### Core Endpoints

- `GET /api/vacancies/` - List job vacancies
- `POST /api/vacancies/` - Create job vacancy
- `GET /api/applications/` - List applications
- `POST /api/applications/` - Submit application
- `GET /api/documents/` - List documents
- `POST /api/documents/` - Upload document

### Example API Usage

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Get vacancies
curl -X GET http://localhost:8000/api/vacancies/ \
  -H "Authorization: Bearer your-jwt-token"
```

## 📱 Mobile App

### Features

- **Authentication**: Secure login and registration
- **Job Search**: Browse and search job listings
- **Applications**: Track application status
- **Documents**: Upload and manage documents
- **Profile**: Manage personal information

### Navigation

The app uses a tab-based navigation with the following screens:

- **Home**: Dashboard with quick actions and statistics
- **Vacancies**: Job search and listing
- **Applications**: Application management
- **Documents**: Document upload and management
- **Profile**: User profile and settings

### Building for Production

```bash
cd frontend

# Build for Android
expo build:android

# Build for iOS
expo build:ios

# Build for web
expo build:web
```

## 🗄️ Database Management

### Migrations

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migration status
python manage.py showmigrations
```

### Database Seeding

```bash
# Populate with test data
python manage.py populate_db

# Clear existing data first
python manage.py populate_db --clear
```

### Backup and Restore

```bash
# Create backup
python manage.py dumpdata > backup.json

# Restore from backup
python manage.py loaddata backup.json
```

## 🐳 Docker Deployment

### Development

```bash
# Build and run development environment
docker-compose -f docker-compose.dev.yml up --build
```

### Production

```bash
# Build and run production environment
docker-compose -f docker-compose.prod.yml up --build
```

### Environment Files

- `docker-compose.yml` - Base configuration
- `docker-compose.dev.yml` - Development overrides
- `docker-compose.prod.yml` - Production overrides

## 🧪 Testing

### Backend Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test core
python manage.py test users

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

## 📊 Monitoring and Logging

### Django Logging

Configure logging in `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'bridgeaid.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Kill process using port 8000
   lsof -ti:8000 | xargs kill -9
   ```

2. **Database migration errors**
   ```bash
   # Reset migrations
   python manage.py migrate --fake-initial
   ```

3. **Mobile app connection issues**
   - Ensure API server is running
   - Check network configuration
   - Verify API_BASE_URL in mobile app

4. **Docker build failures**
   ```bash
   # Clean Docker cache
   docker system prune -a
   ```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React Native
- Write tests for new features
- Update documentation as needed

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

For support and questions:

- Create an issue in the GitHub repository
- Contact the development team
- Check the documentation wiki

## 🙏 Acknowledgments

- Django and Django REST Framework
- React Native and Expo
- React Native Paper for UI components
- All contributors and testers

---

**BridgeAID** - Building bridges to better opportunities 🌉
