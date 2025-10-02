#!/bin/bash

# BridgeAID Docker Startup Script

echo "🚀 Starting BridgeAID Application..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please edit .env file with your settings before running again."
    exit 1
fi

# Choose environment
echo "Select environment:"
echo "1) Development (with hot reload)"
echo "2) Production (optimized)"
read -p "Enter choice [1-2]: " choice

case $choice in
    1)
        echo "🔧 Starting development environment..."
        docker-compose -f docker-compose.dev.yml up --build
        ;;
    2)
        echo "🏭 Starting production environment..."
        docker-compose -f docker-compose.prod.yml up -d --build
        echo "✅ Production environment started!"
        echo "🌐 Application available at: http://localhost"
        echo "📊 Admin panel: http://localhost/admin"
        echo "🔗 API: http://localhost/api/"
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac
