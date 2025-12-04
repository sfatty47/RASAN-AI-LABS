#!/bin/bash
# Quick endpoint test script (run after deployment)

echo "Testing API endpoints..."
echo ""
echo "1. Health check:"
curl -s http://your-railway-url/api/v1/health || echo "Update URL in script"
echo ""
echo "2. Root endpoint:"
curl -s http://your-railway-url/ || echo "Update URL in script"
echo ""
echo "3. API docs available at:"
echo "   http://your-railway-url/docs"
