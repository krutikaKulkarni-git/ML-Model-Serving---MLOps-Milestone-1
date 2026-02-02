#!/bin/bash

echo "Testing FastAPI endpoint..."
curl -X POST "http://127.0.0.1:8001/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
echo ""