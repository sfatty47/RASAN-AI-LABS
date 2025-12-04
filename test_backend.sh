#!/bin/bash

# RASAN AI Labs Backend Testing Script
# Comprehensive endpoint testing for production API

API_URL="https://rasan-ai-labs-production.up.railway.app"
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🧪 Testing RASAN AI Labs Backend API"
echo "======================================"
echo "API URL: $API_URL"
echo ""

# Test 1: Root Endpoint
echo -e "${YELLOW}1. Testing Root Endpoint (GET /)${NC}"
response=$(curl -s "$API_URL/")
if echo "$response" | grep -q "RASAN AI Labs API"; then
    echo -e "${GREEN}✅ Root endpoint working${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ Root endpoint failed${NC}"
    echo "$response"
fi
echo ""

# Test 2: Health Check
echo -e "${YELLOW}2. Testing Health Check (GET /health)${NC}"
response=$(curl -s "$API_URL/health")
if echo "$response" | grep -q "healthy"; then
    echo -e "${GREEN}✅ Health check passing${NC}"
    echo "$response" | python3 -m json.tool
else
    echo -e "${RED}❌ Health check failed${NC}"
    echo "$response"
fi
echo ""

# Test 3: API Documentation
echo -e "${YELLOW}3. Testing API Documentation (GET /docs)${NC}"
status_code=$(curl -s -o /dev/null -w "%{http_code}" "$API_URL/docs")
if [ "$status_code" = "200" ]; then
    echo -e "${GREEN}✅ API documentation available${NC}"
    echo "   Visit: $API_URL/docs"
else
    echo -e "${RED}❌ API documentation not accessible (HTTP $status_code)${NC}"
fi
echo ""

# Test 4: OpenAPI Schema
echo -e "${YELLOW}4. Testing OpenAPI Schema (GET /openapi.json)${NC}"
response=$(curl -s "$API_URL/openapi.json")
if echo "$response" | grep -q "openapi"; then
    echo -e "${GREEN}✅ OpenAPI schema accessible${NC}"
    endpoint_count=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(len(data.get('paths', {})))" 2>/dev/null || echo "N/A")
    echo "   Endpoints found: $endpoint_count"
else
    echo -e "${RED}❌ OpenAPI schema not accessible${NC}"
fi
echo ""

# Test 5: List Available Endpoints
echo -e "${YELLOW}5. Available API Endpoints:${NC}"
echo -e "${GREEN}   • POST /api/v1/upload${NC} - Upload CSV file"
echo -e "${GREEN}   • POST /api/v1/preprocess/{filename}${NC} - Preprocess data"
echo -e "${GREEN}   • POST /api/v1/analyze${NC} - Analyze data"
echo -e "${GREEN}   • POST /api/v1/train${NC} - Train model"
echo -e "${GREEN}   • GET /api/v1/models/{model_id}${NC} - Get model info"
echo -e "${GREEN}   • POST /api/v1/predict${NC} - Make predictions"
echo ""

echo "======================================"
echo -e "${GREEN}✅ Basic connectivity tests complete!${NC}"
echo ""
echo "📚 Next steps:"
echo "   1. Visit $API_URL/docs for interactive API testing"
echo "   2. Test file upload with a sample CSV"
echo "   3. Test the complete ML workflow"
echo ""

