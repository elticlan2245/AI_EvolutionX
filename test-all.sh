#!/bin/bash

echo "🧪 Testing ArchLlama Platform..."

# Test backend health
echo -n "Testing backend health... "
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅"
else
    echo "❌ Failed"
    exit 1
fi

# Test API
echo -n "Testing models API... "
if curl -s http://localhost:8000/api/models | grep -q "models"; then
    echo "✅"
else
    echo "❌ Failed"
    exit 1
fi

# Test frontend
echo -n "Testing frontend... "
if curl -s http://localhost:3000 | grep -q "root"; then
    echo "✅"
else
    echo "❌ Failed"
    exit 1
fi

echo ""
echo "✅ All tests passed!"
