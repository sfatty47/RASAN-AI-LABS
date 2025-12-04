#!/bin/bash

echo "🔍 Checking OpenAI API Key Configuration"
echo "========================================"
echo ""

cd backend

if [ ! -f .env ]; then
    echo "❌ .env file not found in backend/ directory"
    exit 1
fi

echo "✅ .env file exists"
echo ""

# Check if OPENAI_API_KEY is set
if grep -q "^OPENAI_API_KEY=" .env; then
    KEY_LINE=$(grep "^OPENAI_API_KEY=" .env)
    KEY_VALUE="${KEY_LINE#*=}"
    
    if [ -z "$KEY_VALUE" ] || [ "$KEY_VALUE" = "" ]; then
        echo "⚠️  OPENAI_API_KEY is set but EMPTY"
        echo ""
        echo "Current value: OPENAI_API_KEY="
        echo ""
        echo "Fix: Edit backend/.env and add your key:"
        echo "     OPENAI_API_KEY=sk-your-actual-key-here"
    else
        echo "✅ OPENAI_API_KEY is set"
        echo "   Key length: ${#KEY_VALUE} characters"
        echo "   Preview: ${KEY_VALUE:0:10}..."
        echo ""
        echo "💡 Make sure to restart your backend server after adding the key!"
    fi
else
    echo "❌ OPENAI_API_KEY not found in .env file"
    echo ""
    echo "Add this line to backend/.env:"
    echo "OPENAI_API_KEY=sk-your-actual-key-here"
fi

echo ""
echo "To verify the backend sees it, visit:"
echo "http://localhost:8000/api/v1/config/check"

