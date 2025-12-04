#!/bin/bash

# Quick script to start the dashboard
# Run from project root: ./START_DASHBOARD.sh

echo "🚀 Starting RASAN AI Labs Dashboard..."
echo ""

# Check if we're in the right directory
if [ ! -d "frontend" ]; then
    echo "❌ Error: frontend directory not found!"
    echo "   Please run this script from the project root directory"
    exit 1
fi

# Navigate to frontend
cd frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies first..."
    npm install
    echo ""
fi

echo "✅ Starting development server..."
echo "   Dashboard will be available at: http://localhost:3000"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Start the dev server
npm run dev

